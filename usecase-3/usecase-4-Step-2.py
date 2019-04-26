"""
######################################################
#   Client side encryption using data key caching    #
######################################################
"""
import boto3
import os
import sys 
import random
import botocore.session
import aws_encryption_sdk
import subprocess
import boto3
import aws_encryption_sdk

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.x509.oid import NameOID
from cryptography.x509.base import * 

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from aws_encryption_sdk import encrypt, KMSMasterKeyProvider, CachingCryptoMaterialsManager, LocalCryptoMaterialsCache

def main():
    """
    #############################################################
    #     Client side encryption with data key caching          #
    #############################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        s3_client = boto3.client('s3',region)
        kms_client = boto3.client('kms',region)
        
        #######################################################################
        #                                                                     #
        #   The kmsmasterkeyprovider class is used to store the reference to  # 
        #   the customer master key                                           #
        #                                                                     #
        #   The key alias kms_key_cse_usecase_4 that we created in the        #
        #   kms_key_creation.py is being used here                            #
        #                                                                     #
        #######################################################################
        botocore_session = botocore.session.Session()
        botocore_session.set_config_variable('region', region)
        
        kms_kwargs = dict(key_ids=['alias/kms_key_cse_usecase_4'])
        if botocore_session is not None:
            kms_kwargs["botocore_session"] = botocore_session
        kms_master__key_provider = aws_encryption_sdk.KMSMasterKeyProvider(**kms_kwargs)
        
        #############################################################
        #  Setup configuration parameters for the data key cache    #
        #############################################################
        CACHE_CAPACITY = 100
        MAX_ENTRY_AGE_SECONDS = 300.0
        MAX_ENTRY_MESSAGES_ENCRYPTED = 2
        
        ##########################################################################                                   #
        #   A local in memory cache is created with the configured cache         #
        #   parameters                                                           #
        ##########################################################################
        cache = LocalCryptoMaterialsCache(capacity=CACHE_CAPACITY)
        crypto_materials_manager = CachingCryptoMaterialsManager(
            master_key_provider=kms_master__key_provider,
            cache=cache,
            max_age=MAX_ENTRY_AGE_SECONDS,
            max_messages_encrypted=MAX_ENTRY_MESSAGES_ENCRYPTED
        )
        
        ################################################################
        #                                                              #              
        #  Reference to plain text file, client side encrypted file,   #     
        #  plaintext cycled file                                       #
        #                                                              #
        #  plain text cycled means that file was encrypted and then    #
        #  decrypted into plaintext                                    #
        #                                                              #
        ################################################################
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        plaintext_filename_path = current_directory_path + 'plaintext_u.txt'
        
        encrypted_filename_1 = 'encrypted_e_1.txt'
        encrypted_filename_path_1 = current_directory_path + encrypted_filename_1
        
        encrypted_filename_2 = 'encrypted_e_2.txt'
        encrypted_filename_path_2 = current_directory_path + encrypted_filename_2
        
        plaintext_cycled_filename_path_1 = current_directory_path + 'plaintext_u_cycled_1.txt'
        plaintext_cycled_filename_path_2 = current_directory_path + 'plaintext_u_cycled_2.txt'
        encryption_context = {'whatfor':'usecase-4-cse'}
        
        #########################################################################################
        #   encrypt client side using a kms key and cipher text is put into encrypted_e_1.txt   #
        #########################################################################################
        with open(plaintext_filename_path, 'rb') as plaintext, open(encrypted_filename_path_1, 'wb') as ciphertext:
            with aws_encryption_sdk.stream(
                mode='e',
                source=plaintext,
                materials_manager=crypto_materials_manager,
                encryption_context=encryption_context
            ) as encryptor:
                for chunk in encryptor:
                    ciphertext.write(chunk)
                    
        ##########################################################################################
        #   encrypt client side using a kms key and cipher text is put into encrypted_e_2.txt    #
        ########################################################################################## 
        with open(plaintext_filename_path, 'rb') as plaintext, open(encrypted_filename_path_2, 'wb') as ciphertext:
            with aws_encryption_sdk.stream(
                mode='e',
                source=plaintext,
                materials_manager=crypto_materials_manager,
                encryption_context=encryption_context
            ) as encryptor:
                for chunk in encryptor:
                    ciphertext.write(chunk)
        
        ############################################################################################
        #   Decrypt the client side encrypted file encrypted_e_1.txt                               #
        #   The  decrypted file is called plaintext_u_cycled_1.txt                                 #
        #                                                                                          #
        #   Decrypt the client side encrypted file encrypted_e_2.txt                               #
        #   The  decrypted file is called plaintext_u_cycled_2.txt                                 #
        #                                                                                          #
        #   Check whether the plaintext_u.txt,plaintext_u_cycled_1.txt,plaintext_u_cycled_2.txt    #
        #   have the same content                                                                  #
        ############################################################################################            
        with open(encrypted_filename_path_1, 'rb') as ciphertext, open(plaintext_cycled_filename_path_1, 'wb') as plaintext:
            with aws_encryption_sdk.stream(
                mode='d',
                source=ciphertext,
                materials_manager=crypto_materials_manager
            ) as decryptor:
                for chunk in decryptor:
                    plaintext.write(chunk)
                    
        with open(encrypted_filename_path_2, 'rb') as ciphertext, open(plaintext_cycled_filename_path_2, 'wb') as plaintext:
            with aws_encryption_sdk.stream(
                mode='d',
                source=ciphertext,
                materials_manager=crypto_materials_manager
            ) as decryptor:
                for chunk in decryptor:
                    plaintext.write(chunk)
                    
        print "\nModule run was successful !!"
        print "\nPlain text file plaintext_u.txt was encrypted twice !!"
        print "\n Step 2 completed successfully"

        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    