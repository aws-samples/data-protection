"""
############################################################################
#                                                                          #
#   Create a self signed cert                                              #
#                                                                          #
#   In your organization this would be the root cert or intermediate cert  #
#   depending on your pki certificate hierarchy model                      #
#                                                                          #
############################################################################    
"""
from datetime import datetime
from datetime import timedelta
import os
import subprocess
import sys
import random
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
    ######################################################################
    #   Generating the self signed cert                                  #
    #   Packages from cryptography.io which uses openssl in the backed   #
    #   is used here                                                     #
    ######################################################################
    """
    try:
        ssm_client = boto3.client('ssm')
        s3_client = boto3.client('s3')
        
        #####################################################################################
        #   Generating key pair for self signed cert                                        #
        #   Storing private key of self signed cert in an encrypted DynamoDB table          #
        #   so that other python modules can access it                                      #
        #   The private key generated here is for demonstration purposes, the best practice #
        #   is to store private keys on an HSM                                              #
        #####################################################################################
        privkey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        privkey_pem = privkey.private_bytes(encoding=serialization.Encoding.PEM,\
                        format=serialization.PrivateFormat.PKCS8,\
                        encryption_algorithm=NoEncryption())
        
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    
        rootca_serial_number = random.randint(1, 100000)
        
        ssm_client.put_parameter(Name='/dp-workshop/rootca_serial_number',Type='String',Value=str(rootca_serial_number))
        crl_bucket_name = ssm_client.get_parameter(Name='/dp-workshop/crl_bucket_name')['Parameter']['Value']
        s3_client.put_object(Key='root_ca_private_key',
            Bucket=crl_bucket_name,
            Body=privkey_pem,
            ServerSideEncryption='AES256'
        )
        #############################################################
        #  Create the subject and issuer for the self signed cert   #                
        #############################################################
        subject_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, 'rootca-builder'),
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Nevada'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, 'Las Vegas'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'customer'),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, 'customerdept'),
            x509.NameAttribute(NameOID.SERIAL_NUMBER, str(str(rootca_serial_number)))
        ])
               
        issuer_name = subject_name
        
        ##################################################################
        #  Building the self signed cert pem file self-signed-cert.pem   #                
        ##################################################################
        # path_len=0 means this cert can only sign itself, not other certs.
        basic_contraints = x509.BasicConstraints(ca=True, path_length=1)
        pubkey = privkey.public_key()
    
        now = datetime.utcnow()
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject_name)
            .issuer_name(issuer_name)
            .public_key(pubkey)
            .serial_number(rootca_serial_number)
            .not_valid_before(now)
            .not_valid_after(now + timedelta(days=10*365))
            .add_extension(basic_contraints, True)
            .sign(privkey, hashes.SHA256(), default_backend())
        )
        
        cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        self_signed_cert_filename_path = current_directory_path + 'self-signed-cert.pem'
        
        textfile = open(self_signed_cert_filename_path, 'wb')
        textfile.write(cert_pem)
        textfile.close()
        
        print("Success - Self signed certificate file self_signed_cert.pem created")
        print("\nThis self signed certificate will be used in the certificate chain of trust")
        print("\nStep-3 has been successfully completed \n")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)
    
if __name__ == "__main__":
    main()
    