"""
###########################################################################
#   CLIENT SIDE ENCRYPTION - KMS  CLEAN-UP  FOR USECASE-4                 #
#   LET'S DELETE THE BUCKET AND THE OBJECTS THAT WE CREATED FOR USECASE-4 #
#   LET's ALSO DELETE THE FILES LOCALLY CREATED IN THE FILESYSTEM         #
###########################################################################
"""
from pathlib import Path
import subprocess
import sys
import os 
import boto3

def main():
    """
    #############################################################
    #     Client side encryption with data key caching cleanup  #
    #############################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        s3_client = boto3.client('s3', region)
        
        ##########################################################################
        #   REMOVE ALL THE FILES CREATED IN THE LOCAL FILESYSTEM FOR USECASE-4   #
        ##########################################################################
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        
        encrypted_filename_1 = 'encrypted_e_1.txt'
        encrypted_filename_path_1 = current_directory_path + encrypted_filename_1
        
        encrypted_filename_2 = 'encrypted_e_2.txt'
        encrypted_filename_path_2 = current_directory_path + encrypted_filename_2
        
        plaintext_cycled_filename_path_1 = current_directory_path + 'plaintext_u_cycled_1.txt'
        plaintext_cycled_filename_path_2 = current_directory_path + 'plaintext_u_cycled_2.txt'
        enc_context = {'whatfor':'usecase-4-cse'}
    
        if Path(encrypted_filename_path_1).exists():
            os.remove(encrypted_filename_path_1)
            
        if Path(encrypted_filename_path_2).exists():
            os.remove(encrypted_filename_path_2)
            
        if Path(plaintext_cycled_filename_path_1).exists():
            os.remove(plaintext_cycled_filename_path_1)    
            
        if Path(plaintext_cycled_filename_path_2).exists():
            os.remove(plaintext_cycled_filename_path_2)  
        
       ##############################################
       #     Delete all the S3 buckets and objects  #
       ##############################################
    
        # Delete the objects and buckets that were created as part of usecase-1
        response = s3_client.list_buckets()
        for bucket_name in response['Buckets']:
            if bucket_name['Name'].startswith('reinvent-builder') or bucket_name['Name'].startswith('reinvent-builder-bucket-cw-event'):
                try:
                    response = s3_client.get_bucket_tagging(
                        Bucket=bucket_name['Name']
                    )
                except:
                    pass
        
                if 'TagSet' in response: 
                    if (response['TagSet'][0]['Key'] == 'reinvent') and (response['TagSet'][0]['Value'] == 'dataencryption_builderssession'):
                        # Delete the objects stored in S3 within reinvent-builders-bucket
                        response = s3_client.list_objects(
                            Bucket=bucket_name['Name'],
                            )
                            
                        if 'Contents' in response:    
                            for object_name in response['Contents']:    
                                response = s3_client.delete_object(
                                    Bucket=bucket_name['Name'],
                                    Key=object_name['Key']
                                )
                        
                        response = s3_client.delete_bucket(
                        Bucket=bucket_name['Name']
                        )
                        
                if 'TagSet' in response: 
                    if (response['TagSet'][0]['Key'] == 'whatfor') and (response['TagSet'][0]['Value'] == 'usecase-4-cse'):
                        # Delete the objects stored in S3 within buckets that start with reinvent-builder-bucket-cw-event
                        response = s3_client.delete_bucket(
                            Bucket=bucket_name['Name']
                        )
        
        ##############################################
        #     Delete all the keys that were created  #
        ##############################################
        kms_client = boto3.client('kms',region)
        
        response = kms_client.list_aliases(
            Limit=100
        )
        
        alias_exists = False
        for alias in response['Aliases']:
            if alias['AliasName'] == 'alias/kms_key_cse_usecase_4':
                alias_exists = True
        
        if alias_exists == True:
            response = kms_client.describe_key(
                KeyId='alias/kms_key_cse_usecase_4'
            )
            
            kms_key_id = response['KeyMetadata']['KeyId']
            
            # Delete the alias so that a use can run this use-case multiplt times with the same alias
            response_del_alias = kms_client.delete_alias(
                AliasName='alias/kms_key_cse_usecase_4'
            )
            
            if response['KeyMetadata']['KeyState'] != 'PendingDeletion':
                response = kms_client.schedule_key_deletion(
                    KeyId=kms_key_id,
                    PendingWindowInDays=7
                )
        
        print "\n Cleanup Successful" 
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    