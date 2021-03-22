import sys
import boto3
import time

def main():
    
    try:
        #boto3 Setups
        pcaClient = boto3.client('acm-pca')
        acmClient = boto3.client('acm')
        
        #Variables
        domainNames = ['hr.testdomain.com', 'dev.testdomain.com', 'prod.testdomain.com', 'finance.testdomain.com', 'intra.testdomain.com']
        numCerts = len(domainNames)
        #Get Subordinate CA information
        response = pcaClient.list_certificate_authorities(
            MaxResults=20
        )
        
        #Find all certificates with project tag
        response = pcaClient.list_certificate_authorities(
            MaxResults=20
        )
        max = len(response['CertificateAuthorities'])
        for x in range(0, max):
            if response['CertificateAuthorities'][x]['Status'] == 'ACTIVE' and response['CertificateAuthorities'][x]['Type'] == 'SUBORDINATE':
                SubArn = str(response['CertificateAuthorities'][x]['Arn'])
        response = acmClient.list_certificates(
            CertificateStatuses=['ISSUED'],
            MaxItems=30
        )    
        paginator = acmClient.get_paginator('list_certificates')
        for response in paginator.paginate():
            for certificate in response['CertificateSummaryList']:
                try:
                    tagValue = acmClient.list_tags_for_certificate(CertificateArn=certificate['CertificateArn'])['Tags'][0]['Value']
                    if tagValue == 'applicationV1':
                        certArn=certificate['CertificateArn']
                        response = acmClient.describe_certificate(
                            CertificateArn=certArn
                        )
                        CA_arn = response['Certificate']['CertificateAuthorityArn']
                        cert_serial = response['Certificate']['Serial']
              
                    #Revoke certificate
                    response = pcaClient.revoke_certificate(
                        CertificateAuthorityArn=CA_arn,
                        CertificateSerial=cert_serial,
                        RevocationReason='UNSPECIFIED'
                    )
                    response = acmClient.delete_certificate(
                        CertificateArn=certArn
                    )
                    time.sleep(1)
                    print("Certificate revoked.")
                    
                except:
                    print("")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    
    
if __name__ == "__main__":
    main()
