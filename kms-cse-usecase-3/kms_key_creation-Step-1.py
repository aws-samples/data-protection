"""
##########################################################
#     Create KMS key with alias kms_key_cse_usecase_3    #
##########################################################
"""
import subprocess
import sys
import json
import boto3

def main():
    """
    ##########################################################
    #     Create KMS key with alias kms_key_cse_usecase_3    #
    ##########################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        kms_client = boto3.client('kms', region)
        
        # Checking if the CF stack pre-req has been satisfied, if not exit
        cf_client = boto3.client('cloudformation',region)
        response = cf_client.list_stacks(
            StackStatusFilter=[
                'CREATE_COMPLETE',
            ]
        )
        
        cfstacksetup = False
        for stack in response['StackSummaries']:
            if stack['StackName'] == 'data-protection-cse':
                cfstacksetup = True
                
        if cfstacksetup == False:
            print "\nThe Cloudformation stack data-protection-cse required for this usecase has not been created"
            print "\nPlease execute the following steps:\n"
            print "1. execute the command git checkout master\n"
            print "2. Run the python module cf-setup.py \n"
            print "If you have already run cf-setup.py, please wait for the cloudformation stack creation to complete\n"
            exit(0)
   
        account_num = boto3.client('sts').get_caller_identity().get('Account')
    
        key_policy={
         "Version": "2012-10-17",
         "Id": "key-consolepolicy-3",
         "Statement": [
           {
             "Sid": "Enable IAM User Permissions",
             "Effect": "Allow",
             "Principal": {
               "AWS": "arn:aws:iam::" + account_num + ":root"
             },
             "Action": "kms:*",
             "Resource": "*"
           },
           {
             "Sid": "Allow access for Key Administrators",
             "Effect": "Allow",
             "Principal": {
               "AWS": [
                 "arn:aws:iam::" + account_num + ":role/cryptobuildercloudninerole"
               ]
             },
             "Action": [
               "kms:Create*",
               "kms:Describe*",
               "kms:Enable*",
               "kms:List*",
               "kms:Put*",
               "kms:Update*",
               "kms:Revoke*",
               "kms:Disable*",
               "kms:Get*",
               "kms:Delete*",
               "kms:TagResource",
               "kms:UntagResource",
               "kms:ScheduleKeyDeletion",
               "kms:CancelKeyDeletion"
             ],
             "Resource": "*"
           },
           {
             "Sid": "Allow use of the key",
             "Effect": "Allow",
             "Principal": {
               "AWS": [
                 "arn:aws:iam::" + account_num + ":role/cryptobuildercloudninerole"
               ]
             },
             "Action": [
               "kms:Encrypt",
               "kms:Decrypt",
               "kms:ReEncrypt*",
               "kms:GenerateDataKey*",
               "kms:DescribeKey"
             ],
             "Resource": "*"
           },
           {
             "Sid": "Allow attachment of persistent resources",
             "Effect": "Allow",
             "Principal": {
               "AWS": [
                 "arn:aws:iam::" + account_num + ":role/cryptobuildercloudninerole"
               ]
             },
             "Action": [
               "kms:CreateGrant",
               "kms:ListGrants",
               "kms:RevokeGrant"
             ],
             "Resource": "*",
             "Condition": {
               "Bool": {
                 "kms:GrantIsForAWSResource": "true"
               }
             }
           }
         ]
        }
        
        response = kms_client.create_key(
           Policy=json.dumps(key_policy),
           Description='Master key to encrypt objects written to S3',
           KeyUsage='ENCRYPT_DECRYPT',
           Origin='AWS_KMS',
           BypassPolicyLockoutSafetyCheck=False,
           Tags=[
               {
                   'TagKey': 'crypto-aws-encryption',
                   'TagValue': 'builder-aws-session'
               },
           ]
        )
      
        key_id = response['KeyMetadata']['KeyId']
      
        # Setting a key alias
        response = kms_client.create_alias(
           AliasName='alias/kms_key_cse_usecase_3',
           TargetKeyId=key_id
        )
        
        print "\n KMS Master Key with alias name kms_key_cse_usecase_3 successfully created"
        print "\n In the KMS console you should see the key with the alias kms_key_cse_usecase_3"
        print "\n Step 1 completed successfully"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    