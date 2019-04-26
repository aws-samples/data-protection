"""
#####################################################
#   Check for generatedatakey API call for the      #
#   alias/kms_key_cse_usecase_4 KMS master key      #
#####################################################
"""
import subprocess
import sys
import boto3

def main():
    """
    ##############################################################
    #   Using CW events to check for GenerateDataKey calls for   #
    #   the KMS master key  alias/kms_key_cse_usecase_4          #
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
            if bucket['Name'].startswith("reinvent-builder-bucket-cw-event-usecase-4"):
                bucket_name = bucket['Name']
                response = s3_client.get_bucket_tagging(
                    Bucket=bucket_name
                )
                
                if response['TagSet'][0]['Value'] == 'usecase-4-cse':
                    print "GenerateDataKey API Called\n"
                    print "Eventhough plaintext_u.txt file was encrypted twice only one GenerateDataKey API call was made."
                    print "This is because the data key was cached"
                    print "\n Step 3 completed successfully"
                    gendatakey= True
        
        if gendatakey == False:             
            print "\n Re-run this python module until you see the print GenerateDataKey API Called"
            print "\n The GenerateDataKey API call for the key alias kms_key_cse_usecase_4 that you created in Step 1"
            print "\n is being monitored using a CloudWatch event"
            print "\n It should take about 30-45 seconds for the print to appear"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    