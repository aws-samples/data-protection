#######################################
#     Initial environment setup       #
#######################################

import sys 
import os 
import subprocess
import time
import boto3

try:
    
    # client side encryption
    try:
        response = client.describe_stacks(
            StackName='string',
        )
    except:
        response = client.create_stack(
            StackName='string',
            TemplateURL='string',
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ],
        )
        
    # client side encryption with data key caching
    try:
        response = client.describe_stacks(
            StackName='string',
        )
    except:
        response = client.create_stack(
            StackName='string',
            TemplateURL='string',
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ],
        )
        
    # acm pca private certs for domains 
    try:
        response = client.describe_stacks(
            StackName='string',
        )
    except:
        response = client.create_stack(
            StackName='acm-pca-usecase-6',
            TemplateURL='string',
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ],
        )
        
    print "Workshop environment setup was successful"
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)