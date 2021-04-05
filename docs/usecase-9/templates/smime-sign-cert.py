#########################################
#  Learning about using templates       #
#########################################

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
    #  Creating an S/MIME signing certificate          #
    ####################################################
    """
    try:
        acm_pca_client = boto3.client('acm-pca')

        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        print("This step will take about 2 minutes to complete\n")
        
        ###########################################################################################
        #   Getting subordinate_pca_arn for the subordinate CA that you created                   #
        ###########################################################################################
        
        response = acm_pca_client.list_certificate_authorities(
            MaxResults=20
        )
        
        subordinate_pca_arn = None
        # Getting the Subordinate CA Arn that we created during this workshop
        max = len(response['CertificateAuthorities'])
        for x in range(0, max):
            if response['CertificateAuthorities'][x]['Status'] == 'ACTIVE' and response['CertificateAuthorities'][x]['Type'] == 'SUBORDINATE':
                subordinate_pca_arn = str(response['CertificateAuthorities'][x]['Arn'])
        
        if subordinate_pca_arn is None:
            print ("Error: Could not find subordinate certificate")
        else:
            ###########################################################################################
            #   create a key pair for the cert we want to generate                                    #
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
           
    
            ################################################
            #   createa a csr for the S/MIME signing cert  #    
            ################################################
            endpoint_serial_number = random.randint(1, 100000)
            subject_name_csr = x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, 'S/MIME Signing Cert')
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
            
            response = acm_pca_client.issue_certificate(
                ApiPassthrough={
                    'Extensions': {
                        'ExtendedKeyUsage': [
                            {
                                'ExtendedKeyUsageType': 'EMAIL_PROTECTION'
                            },
                        ],
                        'KeyUsage': {
                            'DigitalSignature': True,
                            'NonRepudiation': True
                        },
                        'SubjectAlternativeNames': [
                            {
                                'Rfc822Name': 'myemail@domain.com',
                            },
                        ]
                    },
                    'Subject': {
                        'Country': 'US',
                        'Organization': 'customer',
                        'OrganizationalUnit': 'customerdept',
                        'State': 'Nevada',
                        'CommonName': 'S/MIME',
                        'SerialNumber': str(endpoint_serial_number),
                        'Locality': 'Las Vegas'
                    }
                },
                CertificateAuthorityArn=subordinate_pca_arn,
                Csr= csr_pem,
                SigningAlgorithm= 'SHA256WITHRSA',
                TemplateArn= 'arn:aws:acm-pca:::template/BlankEndEntityCertificate_APIPassthrough/V1',
                Validity={
                    'Value': 180,
                    'Type': 'DAYS'
                },
                IdempotencyToken='dp-workshop-subordinate'
            )
            
            cert_arn = response['CertificateArn']
            time.sleep(30)
            
            ##############################################
            #  Let's get the certificate bytes           #
            ##############################################
            response = acm_pca_client.get_certificate(
                CertificateAuthorityArn=subordinate_pca_arn,
                CertificateArn=cert_arn
            )
            
            current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
            cert_path = current_directory_path + 'email_signing_cert.pem'
            
            textfilecert = open(cert_path, 'wb')
            textfilecert.write(response['Certificate'].encode('utf_8'))
            textfilecert.close()
           
            print("Successfully created S/MIME signing certificate called email_sign_cert.pem \n")
        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()