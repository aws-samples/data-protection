"""
####################################################################################################
# Create DynamoDB table called shared_variables_crypto_builders or storing key value               #
# pairs shared across multiple python modulesshared variables can be private keys,variables        #
# needed for ACM certs etc.Since the nature of stored data is sensitive,the DDB table is encrypted #
####################################################################################################
"""
import subprocess
import sys
import boto3

def main():
    """
    ###################################################################################
    #  DynamoDB table  shared_variables_crypto_builders for storing shared variables  #
    ###################################################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        ddb_client = boto3.client('dynamodb', region)
        # Create DynamoDB table for storing shared variables across python modules
        try:
            ddb_client.describe_table(TableName='shared_variables_crypto_builders')
            print "shared_variables_crypto_builders Table already exists, please delete it before re-running this module"
        except ddb_client.exceptions.ResourceNotFoundException:
            # Since table does not exist create it
            ddb_client.create_table(
                TableName='shared_variables_crypto_builders',
                KeySchema=[
                    {
                        'AttributeName': 'shared_variables',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'session',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'shared_variables',
                        'AttributeType': 'N'
                    },
                    {
                        'AttributeName': 'session',
                        'AttributeType': 'N'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                },
                SSESpecification={
                    'Enabled': True,
                }
            )
            
            print "Pending DynamoDB table creation for storing shared variables"
            waiter = ddb_client.get_waiter('table_exists')
            waiter.wait(TableName='shared_variables_crypto_builders')
            ddb_client.put_item(TableName='shared_variables_crypto_builders', \
                                Item={'shared_variables':{'N':'1000'}, 'session':{'N':'1000'}})
            print "\nshared_variables_crypto_builders DynamoDB table created"
            
            ##########################################################################################
            #  Associate the ec2 instance of the cloud9 environment with the default security group  #
            #  of the VPC so that this Cloud9 environment can route to the ALB within the VPC        #    
            ##########################################################################################
            
            cloud9_instance_id = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/instance-id'])
            vpc_mac_id = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/network/interfaces/macs/'])
            vpc_id = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/network/interfaces/macs/'+ vpc_mac_id + 'vpc-id'])
            print vpc_id
            ec2 = boto3.resource('ec2',region)
            instance = ec2.Instance(cloud9_instance_id)
            
            # Get all the security groups attached to the Cloud9 environment EC2 instance
            all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]  
            ec2_client = boto3.client('ec2',region)
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
            print all_sg_ids
                
            ##############################################################################################
            #  Assign the security group ID list to the cloud9 environment ec2 instance. this list would #
            #  include the default security group                                                        #    
            ##############################################################################################
            instance.modify_attribute(Groups=all_sg_ids)       
            print "\nDefault security group of VPC added to the Cloud9 environment EC2 instance"
            
            ######################################
            #  Create the target group for ALB   #
            ######################################
            for LB in  response['LoadBalancers']:
                response = elbv2_client.describe_tags(
                    ResourceArns=[
                        LB['LoadBalancerArn'],
                    ],
                )
                
            for TagsAlb in  response['TagDescriptions']:
                for Tag in TagsAlb['Tags']:
                    if Tag['Key'] == 'alb-for-what' and Tag['Value'] == 'acm-pca-workshop-usecase-6':
                        # Create a target group for this application load balancer
                        response = elbv2_client.create_target_group(
                            Name='builders-alb-lambda-target-group',
                            TargetType='lambda'
                        )
                        target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
                        
                        # Storing TargetGroupArn in encrypted DDB Table
                        response = ddb_client.update_item(
                            ExpressionAttributeNames={
                                '#tgarn': 'target_group_arn',
                            },
                            ExpressionAttributeValues={
                                ':a': {
                                    'S': target_group_arn,
                                },
                            },
                            Key={
                                'shared_variables': {
                                    'N': '1000',
                                },
                                'session': {
                                    'N': '1000',
                                },
                            },
                            ReturnValues='ALL_NEW',
                            TableName='shared_variables_crypto_builders',
                            UpdateExpression='SET #tgarn = :a',
                        )
    
                        #########################################################################################
                        #  Register the targets with the targegroup that includes configuring the lambda origin #
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
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    