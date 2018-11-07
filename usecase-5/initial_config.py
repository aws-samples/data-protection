#############################################################################
#  Create DynamoDB table called shared_variables_crypto_builders            #
#############################################################################

import boto3
import json
import sys 

try:

  az = subprocess.check_output(['curl','-s','http://169.254.169.254/latest/meta-data/placement/availability-zone'])
  list_az = az.split('-')
  region = list_az[0]+'-'+list_az[1]+'-'+list_az[2][0]
  ddb_client = boto3.client('dynamodb',region)
  
  # Create a DDB table for storing key value pairs shared across multiple python modules
  
    try:
        response = ddb_client.describe_table(TableName='shared_variables_crypto_builders')
        print "shared_variables_crypto_builders Table already exists, please delete it and execute this module again"
    except ddb_client.exceptions.ResourceNotFoundException:
        # Since table does not exist create it
        table = ddb_client.create_table(
            TableName='shared_variables_crypto_builders',
            KeySchema=[
                {
                    'AttributeName': 'shared_variables',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'session',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'shared_variables',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'session',
                    'AttributeType': 'N'
                },
        
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
            SSESpecification={
                'Enabled': True,
            }
        )
        
        print "Pending DynamoDB table creation for storing shared variables"
        
        waiter = ddb_client.get_waiter('table_exists')
        waiter.wait(TableName='shared_variables_crypto_builders')
        
        ddb_client.put_item(TableName='shared_variables_crypto_builders', \
                            Item={'shared_variables':{'N':'1000'},'session':{'N':'1000'}})
        print ("shared_variables_crypto_builders DynamoDB table created")
    
    dbg = 'True'
    
    ########################################################################################
    # Create a DDB table for storing key value pairs shared across multiple python modules #
    # shared variables can be private keys,variables needed for ACM certs etc.             #
    # Since the nature of stored data is sensitive,       the DDB table is encrypted       #
    ########################################################################################
    
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)