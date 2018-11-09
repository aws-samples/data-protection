"""
####################################################################################################
# Create DynamoDB table called shared_variables_crypto_builders or storing key value               #
# pairs shared across multiple python modulesshared variables can be private keys,variables        #
# needed for ACM certs etc.Since the nature of stored data is sensitive,the DDB table is encrypted #
####################################################################################################
"""
import subprocess
import sys
import boto3

def main():
    """
    ###################################################################################
    #  DynamoDB table  shared_variables_crypto_builders for storing shared variables  #
    ###################################################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        ddb_client = boto3.client('dynamodb', region)
        # Create DynamoDB table for storing shared variables across python modules
        try:
            ddb_client.describe_table(TableName='shared_variables_crypto_builders')
            print "shared_variables_crypto_builders Table already exists, please delete it before re-running this module"
        except ddb_client.exceptions.ResourceNotFoundException:
            # Since table does not exist create it
            ddb_client.create_table(
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
                                Item={'shared_variables':{'N':'1000'}, 'session':{'N':'1000'}})
            print "\nshared_variables_crypto_builders DynamoDB table created"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    