"""
#################################################################################
# Create target group for ALB and register lambda target                        #
# Also create S3 bucket for storing CRL (Certificate revocation lists )         #
#################################################################################
"""
import requests
import sys
import boto3
import random
import os
import json 
import time 

def main():

    albNotFound = 1
    try:
        ec2_client = boto3.client('ec2')
        elbv2_client = boto3.client('elbv2')
        lambda_client = boto3.client('lambda')
        ssm_client = boto3.client('ssm')
        s3_client = boto3.client('s3'   )
        s3_control_client = boto3.client('s3control')
        
        response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
        cloud9_instance_id = response.text
        response = requests.get('http://169.254.169.254/latest/meta-data/network/interfaces/macs/')
        vpc_mac_id = response.text
        response = requests.get('http://169.254.169.254/latest/meta-data/network/interfaces/macs/'+ vpc_mac_id + 'vpc-id')
        vpc_id = response.text
        #print vpc_id
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(cloud9_instance_id)
        
        # Get all the security groups attached to the Cloud9 environment EC2 instance
        all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]  
        # Get security group ID for default security group of the VPC in which the Cloud9 environment instance lives
        # Append it to the security group ID list for the instance
        response = ec2_client.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
                {
                    'Name': 'group-name',
                    'Values': [
                        'default',
                    ]
                },
                
            ],
        )
        
        default_sg = response['SecurityGroups'][0]
        all_sg_ids.append(default_sg['GroupId'])    
        #print all_sg_ids
            
        ##############################################################################################
        #  Assign the security group ID list to the cloud9 environment ec2 instance. this list would #
        #  include the default security group                                                        #    
        ##############################################################################################
        instance.modify_attribute(Groups=all_sg_ids)       
        #print "\nDefault security group of VPC added to the Cloud9 environment EC2 instance"
        
        ######################################
        #  Create the target group for ALB   #
        ######################################
        response = elbv2_client.describe_load_balancers()
        for LB in  response['LoadBalancers']:
            response = elbv2_client.describe_tags(
                ResourceArns=[
                    LB['LoadBalancerArn'],
                ],
            )
        
        for TagsAlb in  response['TagDescriptions']:
            for Tag in TagsAlb['Tags']:
                if Tag['Key'] == 'workshop' and Tag['Value'] == 'acm-private-ca':
                    # Create a target group for this application load balancer
                    response = elbv2_client.create_target_group(
                        Name='builders-alb-lambda-target-group',
                        TargetType='lambda'
                    )
                    target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
                    ssm_client.put_parameter(Name='/dp-workshop/target_group_arn',Type='String',Value=target_group_arn)
                    
                    #########################################################################################
                    #  Register the targets with the targetgroup that includes configuring the lambda origin #
                    #########################################################################################
                    response = lambda_client.get_function_configuration(
                        FunctionName='builders-lambda-origin-one'
                    )
                    
                    lambda_origin_arn = response['FunctionArn']
                    
                    # With the targetgroup ARN register the lambda target
                    response = elbv2_client.register_targets(
                        TargetGroupArn=target_group_arn,
                        Targets=[
                            {
                                'Id': lambda_origin_arn
                            },
                        ]
                    )
                    print "\nLambda targets for the ALB successfully registered"
                    albNotFound = 0
                    
        
        #################################################################################
        #   Create an S3 bucket for storing certificate revocation lists(crl)           #
        #                                                                               #
        #   Also tag the bucket so that it can be associated with this builders session #
        #   for cleanup                                                                 #
        #################################################################################
        crl_bucket_name = 'acm-private-ca-crl-bucket' + str(random.randint(1, 100000))
        # Doing the below because locationconstraint does not support all regions today
        region = boto3.Session().region_name
        if 'us-east-1' in region:
            s3_client.create_bucket(Bucket=crl_bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=crl_bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                }
            )
        
        aws_account_id = boto3.client('sts').get_caller_identity()['Account']
        # Removing public acccess block for the AWS account - All S3 buckets
        response = s3_control_client.put_public_access_block(
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            },
            AccountId=aws_account_id
        )
        
        # Removing public acccess block for the CRL bucket
        response = s3_client.put_public_access_block(
            Bucket=crl_bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        
        waiter = s3_client.get_waiter('bucket_exists')
        waiter.wait(Bucket=crl_bucket_name)
        response = s3_client.put_bucket_tagging(
            Bucket=crl_bucket_name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'workshop',
                        'Value': 'acm-private-ca'
                    },
                ]
            }
        )
        
        #################################################################################
        #   ACM service should be able to write/update crl to this S3 bucket            #
        #   therefore we need to put a bucket policy which gives permission to ACM      #
        #                                                                               #
        #   The bucket policy is read from the file called crl_bucket_policy.json       #
        #################################################################################
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        crl_s3_bucket_policy_json = current_directory_path + 'crl_bucket_policy.json'
    
        crl_bucket_policy = json.loads(open(crl_s3_bucket_policy_json, 'rb').read())
        crl_bucket_policy['Statement'][0]['Resource'][0] = unicode("arn:aws:s3:::"+crl_bucket_name+"/*", 'utf_8')
        crl_bucket_policy['Statement'][0]['Resource'][1] = unicode("arn:aws:s3:::"+crl_bucket_name, 'utf_8')
        
        # Set bucket policy CRL S3 bucket
        response = s3_client.put_bucket_policy(
            Bucket=crl_bucket_name,
            Policy=json.dumps(crl_bucket_policy)
        )
        time.sleep(1)
        ssm_client.put_parameter(Name='/dp-workshop/crl_bucket_name',Type='String',Value=crl_bucket_name)
        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        if (albNotFound):
            print "\nError: unable to register Lambda targets for ALB\n"
            sys.exit(1)
        else:
            print "\nStep-1 has been successfully completed \n"                
            sys.exit(0)

if __name__ == "__main__":
    main()
    