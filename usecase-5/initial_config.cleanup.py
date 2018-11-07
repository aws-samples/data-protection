#############################################################################################
#  1. Deleting KMS key used for these usecases                                              #
#                                                                                           #
#  2. Deleting the DynamoDB table used for storing shared variables                         #
############################################################################################# 

import boto3
import json
import sys 

try:
  # LEt's create a boto3 client for the region us-east-1, this ensures that the key is created in us-east-1
    region = 'us-east-1'
    kms_client = boto3.client('kms',region)
    ddb_client = boto3.client('dynamodb',region)
  
    response = kms_client.schedule_key_deletion(
        KeyId='alias/ssekey_reinvent_builders',
        PendingWindowInDays=7
    )
    
    print ("KMS key with alias ssekey_reinvent_builders scheduled for deletion")

  # Create a DDB table for storing key value pairs shared across multiple python modules
    response = ddb_client.delete_table(
        TableName='shared_variables_data_encryption_builder'
    )
  
    print ("shared_variables_data_encryption_builder DyanamoDB table deleted")
      
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)