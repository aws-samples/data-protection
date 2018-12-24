"""
#################################################################################
#  Issuing a certificate for the private domain alb.workshop.com                #
#                                                                               #
#  Signing the webserver csr to obtain the endpoint cert                        #
#  and the certificate chain from acm                                           #
#                                                                               #
#  The endpoint cert and the certificate chain can be used                      #
#  for accomplishing a successful TLS connection from a client to the webserver #
#                                                                               #
#################################################################################
"""
from datetime import datetime
from datetime import timedelta
import os
import subprocess
import sys
import random
import time
import boto3

def main():
    """
    ############################################################################
    #  Issuing a cert from ACM PCA for the private domain alb.workshop.com     #
    ############################################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        elbv2_client = boto3.client('elbv2', region)
        lambda_client = boto3.client('lambda',region)
        ddb_client = boto3.client('dynamodb', region)
        acm_pca_client = boto3.client('acm-pca', region_name=region)
        acm_client = boto3.client('acm', region_name=region)

        ##################################################################################################
        #   Getting subordinate_pca_arn stored in Dynamo DB                                              #
        #   The subordinate pca arn comes from the ACM subordinate PCA created in step 2 and is required #
        #   for issuing certificates                                                                     #
        #   The target group was created in step 1                                                       #
        ##################################################################################################
        response = ddb_client.get_item(
            TableName='shared_variables_crypto_builders',
            Key={
                'shared_variables': {
                    'N': '1000',
                },
                'session': {
                    'N': '1000',
                },
            },
        )
        
        subordinate_pca_arn = response['Item']['subordinate_pca_arn']['S']
        target_group_arn = response['Item']['target_group_arn']['S']
        
        response = acm_client.request_certificate(
            DomainName='alb.workshop.com',
            CertificateAuthorityArn=subordinate_pca_arn
        )
        certificate_arn = response['CertificateArn']
      
        # It takes some time to create the certificate and for the certificate to be active , hence the sleep in the code
        time.sleep(10)
        
        #####################################################################################################
        #   Getting certificate chain for the issued private cert                                           #
        #   The certificate chain is required by clients to trust the HTTPS Connection to alb.workshop.com  #
        #####################################################################################################
        response = acm_client.get_certificate(
            CertificateAuthorityArn=certificate_arn
        )
        
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        cert_chain_path = current_directory_path + 'cert_chain.pem'

        textfilecertchain = open(cert_chain_path, 'w')
        textfilecertchain.write(response['CertificateChain'])
        textfilecertchain.close()
        
        ##################################################################################
        #   Putting the certificate ARN in the shared DDB table to use later for cleanup #
        ##################################################################################
        response = ddb_client.update_item(
            ExpressionAttributeNames={
                '#certarn': 'private_cert_arn',
            },
            ExpressionAttributeValues={
                ':a': {
                    'S': certificate_arn,
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
            UpdateExpression='SET #certarn = :a',
        )
        
        ###########################################################################################
        #   Creating a HTTPS listener for the ALB                                                 #
        #   Associating the certificate and target group with the HTTPS listener                  #
        ###########################################################################################
        response = elbv2_client.describe_load_balancers()
        for LB in  response['LoadBalancers']:
            #print LB['LoadBalancerArn']
            response = elbv2_client.describe_tags(
                ResourceArns=[
                    LB['LoadBalancerArn'],
                ],
            )
            for TagsAlb in  response['TagDescriptions']:
                #print TagsAlb['Tags']
                for Tag in TagsAlb['Tags']:
                    if Tag['Key'] == 'alb-for-what' and Tag['Value'] == 'acm-pca-workshop-usecase-6':
                        # Add a HTTPS listener
                        response = elbv2_client.create_listener(
                            LoadBalancerArn=LB['LoadBalancerArn'],
                            Protocol='HTTPS',
                            Port=443,
                            Certificates=[
                                {
                                    'CertificateArn': certificate_arn
                                },
                            ],
                            DefaultActions=[
                                {
                                    'Type': 'forward',
                                    'TargetGroupArn': target_group_arn,
                                }
                            ]
                        )
                        
                        #######################################################################################
                        #   Putting the listener ARN in the shared DDB table to use later for cleanup later   #
                        #######################################################################################
                        response = ddb_client.update_item(
                            ExpressionAttributeNames={
                                '#listarn': 'listener_arn',
                            },
                            ExpressionAttributeValues={
                                ':a': {
                                    'S': response['Listeners'][0]['ListenerArn'],
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
                            UpdateExpression='SET #listarn = :a',
                        )
        
        print "Successfully attached a HTTPS listener to the ALB"
        print "Subordinate PCA reinvent.builder.subordinate successfully issued a private certificate for the private domain alb.workshop.com"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    