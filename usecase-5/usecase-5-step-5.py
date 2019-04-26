"""
#############################################################################
#   Import signed subordinate CA cert and certificate trustchain into ACM   #
#############################################################################
"""
import os
import subprocess
import sys
import random
import json
import boto3

def main():
    """
    ##################################################################################
    #   Import subordinate CA signed cert and certificate chain into ACM             #
    #                                                                                #
    #   The certificate chain should contain all CA certs upto to the root but not   #       
    #   including the subordinate CA cert                                            #
    #                                                                                #
    #   After this operation subordinate CA changes to ACTIVE STATUS                 #
    #   and it's ready to produce certificates.You can check this in the ACM console #
    ##################################################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        acm_pca_client = boto3.client('acm-pca', region_name=region)
        ddb_client = boto3.client('dynamodb', region)
        
        response = ddb_client.get_item(
            TableName='shared_variables_crypto_builders_usecase_6',
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
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        response = acm_pca_client.import_certificate_authority_certificate(
            CertificateAuthorityArn=subordinate_pca_arn,
            Certificate=open(current_directory_path +'signed_subordinate_ca_cert.pem', 'rb').read(),
            CertificateChain=open(current_directory_path + 'self-signed-cert.pem', 'rb').read(),
        )
        
        print "Successfully imported signed cert and certificate chain into ACM"
        print "\nStep-5 has been successfully completed \n"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    