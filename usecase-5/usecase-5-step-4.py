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
        acm_pca_client = boto3.client('acm-pca')
        ssm_client = boto3.client('ssm')
        s3_client = boto3.client('s3')
        
        #####################################################################################
        #   Get the self signed CA cert private key, cert serial numbers from the DynamoDB  #  
        #   table. These are required for signing the subordinate private CA csr            #
        #####################################################################################   
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'

        root_ca_serial_number = int(ssm_client.get_parameter(Name='/dp-workshop/rootca_serial_number')['Parameter']['Value'])
        subordinate_ca_serial_number = int(ssm_client.get_parameter(Name='/dp-workshop/subordinate_ca_serial_number')['Parameter']['Value'])
        subordinate_pca_arn = ssm_client.get_parameter(Name='/dp-workshop/subordinate_pca_arn')['Parameter']['Value']
        #####################################################################################
        #   The private key used here is for demonstration purposes, the best practice      #
        #   is to store private keys on an HSM                                              #
        #####################################################################################
        bucket_name = ssm_client.get_parameter(Name='/dp-workshop/crl_bucket_name')['Parameter']['Value']
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key='root_ca_private_key'
        )
        root_ca_private_key = serialization.load_pem_private_key(
                response['Body'].read(),
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
        
        csr = x509.load_pem_x509_csr(response['Csr'].encode('utf_8'), default_backend())
        
        #####################################################################
        #   Sign the subordinate private CA CSR using the self signed cert  #  
        #####################################################################
        issuer_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, 'rootca-builder'),
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Nevada'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, 'Las Vegas'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'customer'),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, 'customerdept'),
            x509.NameAttribute(NameOID.SERIAL_NUMBER, str(str(root_ca_serial_number)))
        ])
               
        subject_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, 'dp-workshop.subordinate'),
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Nevada'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, 'Las Vegas'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'customer'),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, 'customerdept'),
            x509.NameAttribute(NameOID.SERIAL_NUMBER, str(str(subordinate_ca_serial_number)))
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
    
        signed_subordinate_ca_cert_filename_path = current_directory_path + 'signed_subordinate_ca_cert.pem'
        
        textfile = open(signed_subordinate_ca_cert_filename_path, 'wb')
        textfile.write(cert_pem)
        textfile.close()
        
        print("Successfully created signed subordinate CA pem file signed_subordinate_ca_cert.pem")
        print("\nStep-4 has been successfully completed \n")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    