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
###############################################################################
"""
import os
import subprocess
import sys
from pathlib import Path
import time
import boto3
from botocore.exceptions import ClientError

def main():
    """
    ###########################################
    # Cleanup all resources that were created #
    ###########################################
    """
    try:
        s3_client = boto3.client('s3')
        acm_pca_client = boto3.client('acm-pca')
        ssm_client = boto3.client('ssm')
        elbv2_client = boto3.client('elbv2')
        acm_client = boto3.client('acm')
        
        ####################################################################################
        #  Remove all the files created in the local filesystem as part of this usecase    #
        ####################################################################################
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        print("\nThis step takes about 45 seconds to complete \n")

        self_signed_cert_filename_path = current_directory_path + 'self-signed-cert.pem'
        signed_subordinate_ca_cert_filename_path = current_directory_path + 'signed_subordinate_ca_cert.pem'
        cert_chain_filename_path = current_directory_path + 'cert_chain.pem'

        if Path(self_signed_cert_filename_path).exists():
            os.remove(self_signed_cert_filename_path)
            
        if Path(signed_subordinate_ca_cert_filename_path).exists():
            os.remove(signed_subordinate_ca_cert_filename_path)
    
        if Path(cert_chain_filename_path).exists():
            os.remove(cert_chain_filename_path) 
            
        try:
            subordinate_pca_arn = ssm_client.get_parameter(Name='/dp-workshop/subordinate_pca_arn')['Parameter']['Value']
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
        except:
            print("No PCA to delete and clean up !!")
        
        ###################################################
        #   remove all the s3 buckets that were created   #
        ###################################################
        try:
            crl_bucket_name = ssm_client.get_parameter(Name='/dp-workshop/crl_bucket_name')['Parameter']['Value']
            try:
                response = s3_client.list_objects(Bucket=crl_bucket_name)
                if 'Contents' in response:    
                    for object_name in response['Contents']:    
                        response = s3_client.delete_object(
                            Bucket=crl_bucket_name,
                            Key=object_name['Key']
                        )
                response = s3_client.delete_bucket(Bucket=crl_bucket_name)
            except ClientError:
                print('no bucket to clean up: '+crl_bucket_name)
        except ClientError:
            print('no parameter value: /dp-workshop/crl_bucket_name')

        #####################################################################################################################################
        #   Remove HTTPS listener for the ALB, remove the TargetGroup, cleanup default security group from the ALB and cloud9 environment   #
        #####################################################################################################################################
        
        # Deleting the listener created for the ALB
        try:
            listener_arn = ssm_client.get_parameter(Name='/dp-workshop/listener_arn')['Parameter']['Value']
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
            print("No HTTPS listener found to delete and clean up !!")
         
        # Deleting the target groups created for the ALB
        try:
            target_group_arn = ssm_client.get_parameter(Name='/dp-workshop/target_group_arn')['Parameter']['Value']
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
            print("No Target group found for the ALB to delete and clean up !!")
        
        time.sleep(20)
        # Deleting the certificates created for the HTTPS listener of the ALB
        try:
            private_cert_arn = ssm_client.get_parameter(Name='/dp-workshop/private_cert_arn')['Parameter']['Value']
            response = acm_client.describe_certificate(
                CertificateArn=private_cert_arn
            )
            
            if response is not None:
                response = acm_client.delete_certificate(
                    CertificateArn=private_cert_arn
                )
        except:
            print("No private certificates for the private domain alb.workshop.com mapping to the ALB")

        params = ['/dp-workshop/listener_arn',
            '/dp-workshop/private_cert_arn',
            '/dp-workshop/target_group_arn',
            '/dp-workshop/subordinate_pca_arn',
            '/dp-workshop/rootca_serial_number',
            '/dp-workshop/subordinate_ca_serial_number',
            '/dp-workshop/crl_bucket_name'
        ]
        for param in params: 
            try: 
                ssm_client.delete_parameter(Name=param)
            except ClientError as e:
                print(("Parameter "+param+" not found in store, not deleted"))       
            
        print("\nEverything cleaned up, you are all good !!\n")
        print("\nStep-9 cleanup has been successfully completed \n")

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)
 

if __name__ == "__main__":
    main()
    