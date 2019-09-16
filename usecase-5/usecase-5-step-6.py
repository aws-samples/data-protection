"""
#################################################################################
#  Issuing a certificate for the private domain alb.workshop.com                #
#                                                                               #
#  The endpoint cert and the certificate chain can be used                      #
#  for accomplishing a successful TLS connection from a client to the webserver #
#                                                                               #
#################################################################################
"""
from datetime import datetime
from datetime import timedelta
import os
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
        elbv2_client = boto3.client('elbv2')
        lambda_client = boto3.client('lambda')
        ssm_client = boto3.client('ssm')
        acm_pca_client = boto3.client('acm-pca')
        acm_client = boto3.client('acm')

        ##################################################################################################
        #   Retrieve subordinate_pca_arn                                                                 #
        #   The subordinate pca arn comes from the ACM subordinate PCA created in step 2 and is required #
        #   for issuing certificates                                                                     #
        #   The target group was created in step 1                                                       #
        ##################################################################################################

        subordinate_pca_arn = ssm_client.get_parameter(Name='/dp-workshop/subordinate_pca_arn')['Parameter']['Value']
        target_group_arn = ssm_client.get_parameter(Name='/dp-workshop/target_group_arn')['Parameter']['Value']

        response = acm_client.request_certificate(
            DomainName='alb.workshop.com',
            CertificateAuthorityArn=subordinate_pca_arn
        )
        certificate_arn = response['CertificateArn']
      
        print("Attaching HTTPS listener to ALB and requesting certificate for the private domain alb.workshop.com\n")
        print("This step takes about a minute to complete\n")

        # It takes some time to create the certificate and for the certificate to be active , hence the sleep in the code
        time.sleep(5)
        
        #####################################################################################################
        #   Getting certificate chain for the issued private cert                                           #
        #   The certificate chain is required by clients to trust the HTTPS Connection to alb.workshop.com  #
        #####################################################################################################
        response = acm_client.get_certificate(
            CertificateArn=certificate_arn
        )
        
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        cert_chain_path = current_directory_path + 'cert_chain.pem'

        textfilecertchain = open(cert_chain_path, 'wb')
        textfilecertchain.write(response['CertificateChain'].encode('utf_8'))
        textfilecertchain.close()
        
        ##################################################################################
        #   Putting the certificate ARN in the parameter store to use later for cleanup  #
        ##################################################################################
        ssm_client.put_parameter(Name='/dp-workshop/private_cert_arn',Type='String',Value=certificate_arn)

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
                    if Tag['Key'] == 'workshop' and Tag['Value'] == 'data-protection':
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
                        #   Putting the listener ARN in the parameter store to use later for cleanup later    #
                        #######################################################################################
                        ssm_client.put_parameter(Name='/dp-workshop/listener_arn',Type='String',Value=response['Listeners'][0]['ListenerArn'])

        time.sleep(60)
        print("Successfully attached a HTTPS listener to the ALB")
        print("\nSuccessfully issued a private certificate for the private domain alb.workshop.com")
        print("\nStep-6 has been successfully completed \n")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    