"""
###########################################################
#   Client side encryption and decryption using KMS keys  #
###########################################################
"""
import subprocess
import sys
import os
import botocore.session
import aws_encryption_sdk

def main():
    """
    ###################################
    #     client side encryption      #
    ###################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        
        #######################################################################
        #   The kmsmasterkeyprovider class is used to store the reference to  # 
        #   the customer master key                                           #
        #                                                                     #
        #   The key alias kms_key_cse_usecase_3 that we created in the        #
        #   kms_key_creation.py is being used here                            #
        #######################################################################
        botocore_session = botocore.session.Session()
        botocore_session.set_config_variable('region', region)
        
        kms_kwargs = dict(key_ids=['alias/kms_key_cse_usecase_3'])
        if botocore_session is not None:
            kms_kwargs["botocore_session"] = botocore_session
        kms_master__key_provider = aws_encryption_sdk.KMSMasterKeyProvider(**kms_kwargs)
        
        ################################################################
        #                                                              #              
        #  Reference to plain text file, client side encrypted file,   #     
        #  and plaintext cycled file                                   #
        #                                                              #
        #  plain text cycled means that file was encrypted and then    #
        #  decrypted into plaintext                                    #
        #                                                              #
        ################################################################
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        plaintext_filename_path = current_directory_path + 'plaintext_u.txt'
        
        encrypted_filename = 'encrypted_e.txt'
        encrypted_filename_path = current_directory_path + encrypted_filename
        
        plaintext_cycled_filename_path = current_directory_path + 'plaintext_u_cycled.txt'
        encryption_context = {'whatfor':'usecase-3-cse'}
        
        #########################################################################################
        #   encrypt client side using a kms key and cipher text is put into encrypted_e.txt   #
        #########################################################################################
        with open(plaintext_filename_path, 'rb') as plaintext, open(encrypted_filename_path, 'wb') as ciphertext:
            with aws_encryption_sdk.stream(
                mode='e',
                source=plaintext,
                key_provider=kms_master__key_provider,
                encryption_context=encryption_context
            ) as encryptor:
                for chunk in encryptor:
                    ciphertext.write(chunk)
                    
        #################################################################
        #   Decrypt the s3 cycled file encrypted_e.txt                  #
        #   The  decrypted file is called plaintext_u_cycled.txt        #
        #################################################################
        with open(encrypted_filename_path, 'rb') as ciphertext, open(plaintext_cycled_filename_path, 'wb') as plaintext:
            with aws_encryption_sdk.stream(
                mode='d',
                source=ciphertext,
                key_provider=kms_master__key_provider
            ) as decryptor:
                #print decryptor.header.encryption_context
                for chunk in decryptor:
                    plaintext.write(chunk)
                    
        print "\nModule run was successful !!"
        print "\nYou should see the client side encrypted file encrypted_e.txt !!"
        print "\nYou should see the cycled file plaintext_u_cycled.txt !!"
        print "\n Step 2 completed successfully"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    