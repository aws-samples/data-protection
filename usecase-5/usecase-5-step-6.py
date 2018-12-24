"""
#################################################################################
#  Creating a csr for an web server endpoint                                    #
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

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import NoEncryption

def main():
    """
    ####################################################
    #  Creating a server cert for a flask web server   #
    ####################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        acm_pca_client = boto3.client('acm-pca', region_name=region)
        ddb_client = boto3.client('dynamodb', region)
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        
        ###########################################################################################
        #   Getting subordinate_pca_arn stored in dynamo DB                                       #
        #   The subordinate pca arn created in part 1 is required for issuing certificates        #
        ###########################################################################################
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
        
        ###########################################################################################
        #   create a key pair for the webserver endpoint                                          #
        #   The private key portion of the key pair is required for signing the webserver CSR     #
        #   The private key used here is for demonstration purposes, the best practice            #
        #   is to store private keys on an HSM                                                    #
        ###########################################################################################
        csr_webserver_privkey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        csr_webserver_privkey_pem = csr_webserver_privkey.private_bytes(encoding=serialization.Encoding.PEM,\
                        format=serialization.PrivateFormat.PKCS8,\
                        encryption_algorithm=NoEncryption())
                        
        response = ddb_client.update_item(
            ExpressionAttributeNames={
                '#wep': 'webserver_endpoint_privatekey',
            },
            ExpressionAttributeValues={
                ':b': {
                    'B': csr_webserver_privkey_pem,
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
            UpdateExpression='SET #wep = :b',
        )
       

        ###########################################################################################
        #   createa a csr for the webserver endpoint 127.0.0.1                                    #
        #                                                                                         #
        #   A simple flask webserver is the endpoint here                                         #
        #                                                                                         #
        #   We are not using domain names in this example because obtaining a domain name takes   #
        #   time, therefore we are using 127.0.0.1 as the common name within the CSR subject      #
        #   This is purely for demonstration purposes                                             #
        ###########################################################################################
        endpoint_serial_number = random.randint(1, 100000)
        subject_name_csr = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'127.0.0.1'),
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Nevada'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'Las Vegas'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'customer'),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'customerdept'),
            x509.NameAttribute(NameOID.SERIAL_NUMBER, unicode(str(endpoint_serial_number)))
        ])
    
        # ca=False for non ca Certs
        basic_contraints = x509.BasicConstraints(ca=False, path_length=None)
        csr = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(subject_name_csr)
            .add_extension(basic_contraints, True)
            .sign(csr_webserver_privkey, hashes.SHA256(), default_backend())
        )
        
        csr_pem = csr.public_bytes(encoding=serialization.Encoding.PEM)
        
        ############################################################################################
        #                                                                                          #    
        #   ACM issues a certificate for the webserver endpoint that's valid for 6 months          #
        #   or 180 days                                                                            #
        #                                                                                          #
        #   Currently waiters are not available for ACM,therefore sleeping for 30 seconds so that  #                                      #
        #   certificate is issued. The reason for the sleep is that issuing the certificate        #
        #   takes a few seconds                                                                    #
        #                                                                                          #
        ############################################################################################
        response = acm_pca_client.issue_certificate(
            CertificateAuthorityArn=subordinate_pca_arn,
            Csr=csr_pem,
            SigningAlgorithm='SHA256WITHRSA',
            Validity={
                'Value': 180,
                'Type': 'DAYS'
            },
            IdempotencyToken='reinvent-builder-subordinate'
        )
        
        cert_arn = response['CertificateArn']
        time.sleep(30)
        
        ##########################################################################################
        #   1.The web server endpoint cert  file is called webserver_cert.pem                    #
        #                                                                                        #
        #   2.The certificate chain file is called webserver_cert_chain.pem                      #
        #                                                                                        #
        #   3.The pem key file webserver_privkey.pem contains the private key for the webserver  #     
        #     private keys shoud not be stored in files ,best practice is to store it on an HSM  #
        ##########################################################################################
        response = acm_pca_client.get_certificate(
            CertificateAuthorityArn=subordinate_pca_arn,
            CertificateArn=cert_arn
        )
        
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        webserver_cert_path = current_directory_path + 'webserver_cert.pem'
        webserver_cert_chain_path = current_directory_path + 'webserver_cert_chain.pem'
        webserver_privkey_path = current_directory_path + 'webserver_privkey.pem'
    
        textfilecert = open(webserver_cert_path, 'w')
        textfilecert.write(response['Certificate'])
        textfilecert.close()
        
        textfilecertchain = open(webserver_cert_chain_path, 'w')
        textfilecertchain.write(response['CertificateChain'])
        textfilecertchain.close()
        
        textfilecertchain = open(webserver_privkey_path, 'w')
        textfilecertchain.write(csr_webserver_privkey_pem)
        textfilecertchain.close()
        
        print "Successfully created server certificate webserver_cert.pem for the flask web server\n"
        print "Successfully created chain of trust for the flask web server"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    