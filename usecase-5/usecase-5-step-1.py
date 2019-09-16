"""
#################################################################################
# Create target group for ALB and register lambda target                        #
#################################################################################
"""
import requests
import sys
import boto3

def main():

    albNotFound = 1
    try:
        ec2_client = boto3.client('ec2')
        elbv2_client = boto3.client('elbv2')
        lambda_client = boto3.client('lambda')
        ssm_client = boto3.client('ssm')
        
        cf_client = boto3.client('cloudformation')
        response = cf_client.list_stacks(
            StackStatusFilter=[
                'CREATE_COMPLETE',
            ]
        )
        
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
                if Tag['Key'] == 'workshop' and Tag['Value'] == 'data-protection':
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
                    print("\nLambda targets for the ALB successfully registered")
                    albNotFound = 0
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        if (albNotFound):
            print("\nError: unable to register Lambda targets for ALB\n")
            sys.exit(1)
        else:
            print("\nStep-1 has been successfully completed \n")                
            sys.exit(0)

if __name__ == "__main__":
    main()
    