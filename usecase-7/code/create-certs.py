import sys
import boto3

def main():
    
    try:
        #boto3 Setups
        client = boto3.client('acm-pca')
        acmClient = boto3.client('acm')
        
        #Variables
        domainNames = ['hr.testdomain.com', 'dev.testdomain.com', 'prod.testdomain.com', 'finance.testdomain.com', 'intra.testdomain.com']
        numCerts = len(domainNames)
        #Get Subordinate CA information
        response = client.list_certificate_authorities(
            MaxResults=20
        )
        SubArn = None
        max = len(response['CertificateAuthorities'])
        for x in range(0, max):
            if response['CertificateAuthorities'][x]['Status'] == 'ACTIVE' and response['CertificateAuthorities'][x]['Type'] == 'SUBORDINATE':
                SubArn = str(response['CertificateAuthorities'][x]['Arn'])
        
        if SubArn is None:
            print ("Error: Could not find subordinate certificate")
        else:
            #Get Subordinate CA CSR
            csr = client.get_certificate_authority_csr(
                CertificateAuthorityArn=SubArn
            )
                
            #Generate private end entity certificates
            for x in range(0, numCerts):
                response = acmClient.request_certificate(
                    DomainName=domainNames[x],
                    IdempotencyToken= str(x),
                    Options={
                        'CertificateTransparencyLoggingPreference': 'ENABLED'
                    },
                    CertificateAuthorityArn=SubArn
                )
                tagResponse = acmClient.add_tags_to_certificate(
                    CertificateArn=response['CertificateArn'],
                    Tags=[
                        {
                            'Key': 'project',
                            'Value': 'applicationV1'
                        },
                    ]
                )
                print(response['CertificateArn'])
            print('Certificates created. Navigate to ACM Console.')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    
    
if __name__ == "__main__":
    main()
