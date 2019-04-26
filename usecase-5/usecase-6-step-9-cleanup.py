"""
###############################################################################
#  Cleanup all resources created within python modules for ACM usecase-6      #
#                                                                             #
#  1. S3 buckets used for CRL(Certificate revocation list)                    #
#                                                                             #
#  2. The private certifiate authority is deleted                             #
#                                                                             #
#  3. All the files created in the filesystem is deleted                      #
#                                                                             #
#  4. CF stack acm-pca-usecase-6 is deleted                                   #
#                                                                             #
###############################################################################
"""
import os
import subprocess
import sys
from pathlib import Path
import time
import boto3

def main():
    """
    ###########################################
    # Cleanup all resources that were created #
    ###########################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        s3_client = boto3.client('s3', region_name=region)
        acm_pca_client = boto3.client('acm-pca', region_name=region)
        ddb_client = boto3.client('dynamodb', region)
        elbv2_client = boto3.client('elbv2', region)
        acm_client = boto3.client('acm', region_name=region)
        
        ####################################################################################
        #  Remove all the files created in the local filesystem as part of this usecase    #
        ####################################################################################
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        print "\nThis step takes about 45 seconds to complete \n"

        self_signed_cert_filename_path = current_directory_path + 'self-signed-cert.pem'
        signed_subordinate_ca_cert_filename_path = current_directory_path + 'signed_subordinate_ca_cert.pem'
        cert_chain_path = current_directory_path + 'cert_chain.pem'
       
        if Path(self_signed_cert_filename_path).exists():
            os.remove(self_signed_cert_filename_path)
            
        if Path(signed_subordinate_ca_cert_filename_path).exists():
            os.remove(signed_subordinate_ca_cert_filename_path)
    
        if Path(cert_chain_path).exists():
            os.remove(cert_chain_path)    
       
        ##########################################
        #  Delete the subordinate pca created    #
        ##########################################
        subordinate_pca_arn = None 
        target_group_arn = None
        private_cert_arn = None
        listener_arn = None
        try:
            response = ddb_client.describe_table(TableName='shared_variables_crypto_builders_usecase_6')
            if response is not None:
                response = ddb_client.get_item(TableName='shared_variables_crypto_builders_usecase_6', \
                    Key={
                            'shared_variables': {
                                'N': '1000',
                            },
                            'session': {
                                'N': '1000',
                            },
                        },
                )
                                
                if  'subordinate_pca_arn' in response['Item']:
                    subordinate_pca_arn = response['Item']['subordinate_pca_arn']['S']
                
                if  'target_group_arn' in response['Item']:
                    target_group_arn = response['Item']['target_group_arn']['S']
                
                if  'private_cert_arn' in response['Item']:
                    private_cert_arn = response['Item']['private_cert_arn']['S']
                
                if  'listener_arn' in response['Item']:
                    listener_arn = response['Item']['listener_arn']['S']
                
                # Delete the DDB Table that stores key value pairs shared across multiple python modules
                response = ddb_client.delete_table(
                    TableName='shared_variables_crypto_builders_usecase_6'
                )
        except ddb_client.exceptions.ResourceNotFoundException:
            print "No DDB table found to delete !! that's OK"
            
        if subordinate_pca_arn is not None:
            response = acm_pca_client.describe_certificate_authority(
                CertificateAuthorityArn=subordinate_pca_arn
            )
            
            if response['CertificateAuthority']['Status'] != 'DELETED':
                if response['CertificateAuthority']['Status'] == 'ACTIVE':
                    response = acm_pca_client.update_certificate_authority(
                        CertificateAuthorityArn=subordinate_pca_arn,
                        Status='DISABLED'
                    )
                
                response = acm_pca_client.delete_certificate_authority(
                    CertificateAuthorityArn=subordinate_pca_arn,
                    PermanentDeletionTimeInDays=7
                )
                time.sleep(20)
        
        ###################################################
        #   remove all the s3 buckets that were created   #
        ###################################################
        response = s3_client.list_buckets()
        for bucket_name in response['Buckets']:
            if bucket_name['Name'].startswith('builder-acm-pca-usecase-6-bucket-pca-crl'):
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
        
        #####################################################################################################################################
        #   Remove HTTPS listener for the ALB, remove the TargetGroup, cleanup default security group from the ALB and cloud9 environment   #
        #####################################################################################################################################
        
        # Deleting the listener created for the ALB
        try:
            response = elbv2_client.describe_listeners(
                ListenerArns=[
                    listener_arn,
                ],
            )
            
            if response is not None:
                response = elbv2_client.delete_listener(
                    ListenerArn=listener_arn
                )
        except:
            print "No HTTPS listener found to delete and clean up !!"
         
        # Deleting the target groups created for the ALB
        try:
            response = elbv2_client.describe_target_groups(
                TargetGroupArns=[
                    target_group_arn,
                ],
            )
            
            if response is not None:
                response = elbv2_client.delete_target_group(
                    TargetGroupArn=target_group_arn
                )
        except:
            print "No Target group found for the ALB to delete and clean up !!"
        
        time.sleep(20)
        # Deleting the certificates created for the HTTPS listener of the ALB
        try:
            response = acm_client.describe_certificate(
                CertificateArn=private_cert_arn
            )
            
            if response is not None:
                response = acm_client.delete_certificate(
                    CertificateArn=private_cert_arn
                )
        except:
            print "No private certificates for the private domain alb.workshop.com mapping to the ALB"

        ###########################################
        #  Cleanup the cloudformation template    #
        ###########################################
        # cf_client = boto3.client('cloudformation',region)
        # response = cf_client.list_stacks(
        #     StackStatusFilter=[
        #         'CREATE_COMPLETE',
        #     ]
        # )
        
        # for stack in response['StackSummaries']:
        #     if stack['StackName'] == 'acm-pca-usecase-6':
        #         response = cf_client.delete_stack(
        #             StackName='acm-pca-usecase-6',
        #         )
        
        #print "\nDeleting Cloudformation stack created for this usecase has been initiated .It takes about 3 minutes for the CF stack to be deleted"
        print "\nEverything cleaned up ,you are all good !!\n"
        print "\nStep-9 cleanup has been successfully completed \n"
        # print "\nif you plan to re-run this usecase after cleanup please wait until the CF stack named acm-pca-usecase-6 has been deleted \n"
    
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
 

if __name__ == "__main__":
    main()
    