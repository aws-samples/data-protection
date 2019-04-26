"""
#################################################################################
#   Sign the subordinate acm pca csr using the self signed cert                      #
#                                                                               #
#   Within your organization this might be a root CA cert or an intermediate CA #
#   cert                                                                        #
#################################################################################    
"""
from datetime import datetime
from datetime import timedelta
import os
import subprocess
import sys
import boto3

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID

def main():
    """
    #################################
    #  Sign subordinate acm pca csr #
    #################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        acm_pca_client = boto3.client('acm-pca', region_name=region)
        ddb_client = boto3.client('dynamodb', region)
        
        #####################################################################################
        #   Get the self signed CA cert private key, cert serial numbers from the DynamoDB  #  
        #   table. These are required for signing the subordinate private CA csr            #
        #####################################################################################   
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
       
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
                        
        root_ca_serial_number = response['Item']['rootca_serial_number']['N']
        subordinate_ca_serial_number = int(response['Item']['subordinate_ca_serial_number']['N'])
        subordinate_pca_arn = response['Item']['subordinate_pca_arn']['S']
        
        #####################################################################################
        #   The private key used here is for demonstration purposes, the best practice      #
        #   is to store private keys on an HSM                                              #
        #####################################################################################
        root_ca_private_key = serialization.load_pem_private_key(
            response['Item']['root_ca_private_key']['B'],
            password=None,
            backend=default_backend() 
        )
        
        #####################################################################################
        #   Get the subordinate CA CSR from ACM                                             #  
        #   Load the CSR into a format that the crytography.io package understands          #
        ##################################################################################### 
        response = acm_pca_client.get_certificate_authority_csr(
            CertificateAuthorityArn=subordinate_pca_arn
        )
        
        csr = x509.load_pem_x509_csr(str(response['Csr']), default_backend())
        
        #####################################################################
        #   Sign the subordinate private CA CSR using the self signed cert  #  
        #####################################################################
        issuer_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'rootca-builder'),
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Nevada'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'Las Vegas'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'customer'),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'customerdept'),
            x509.NameAttribute(NameOID.SERIAL_NUMBER, unicode(str(root_ca_serial_number)))
        ])
               
        subject_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'acmpcausecase6.subordinate'),
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Nevada'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'Las Vegas'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'customer'),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'customerdept'),
            x509.NameAttribute(NameOID.SERIAL_NUMBER, unicode(str(subordinate_ca_serial_number)))
        ])
    
        basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
        
        ##########################################################################################
        #   Put the signed subordinate CA cert into a file named signed_subordinate_ca_cert.pem  #  
        ########################################################################################## 
        now = datetime.utcnow()
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject_name)
            .issuer_name(issuer_name)
            .public_key(csr.public_key())
            .serial_number(subordinate_ca_serial_number)
            .not_valid_before(now)
            .not_valid_after(now + timedelta(days=10*365))
            .add_extension(basic_contraints, True)
            .sign(root_ca_private_key, hashes.SHA256(), default_backend())
        )
        
        cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        signed_subordinate_ca_cert_filename_path = current_directory_path + 'signed_subordinate_ca_cert.pem'
        
        textfile = open(signed_subordinate_ca_cert_filename_path, 'w')
        textfile.write(cert_pem)
        textfile.close()
        
        print "Successfully created signed subordinate CA pem file signed_subordinate_ca_cert.pem"
        print "\nStep-4 has been successfully completed \n"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    