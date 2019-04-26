"""
#####################################################
#   Check for generatedatakey API call for the      #
#   alias/kms_key_cse_usecase_3 KMS master key      #
#####################################################
"""
import subprocess
import sys
import boto3

def main():
    """
    ##############################################################
    #   Using CW events to check for GenerateDataKey calls for   #
    #   the KMS master key  alias/kms_key_cse_usecase_3          #
    ##############################################################
    """
    try:
        gendatakey = False
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        s3_client = boto3.client('s3', region)
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'].startswith("reinvent-builder-bucket-cw-event"):
                bucket_name = bucket['Name']
                response = s3_client.get_bucket_tagging(
                    Bucket=bucket_name
                )
                
                if response['TagSet'][0]['Value'] == 'usecase-3-cse':
                    print "GenerateDataKey API Called"
                    print "\nStep 3 completed successfully"
                    gendatakey= True
                    
        if gendatakey == False:          
            print "\n Re-run this python module until the GenerateDataKey API called print appears"
            print "\n The GenerateDataKey API call for the key alias kms_key_cse_usecase_3 that you created in Step 1"
            print "\n is being monitored using a CloudWatch event"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    