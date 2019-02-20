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
            StackName='data-protection-cse',
        )
    except:
        response = client.create_stack(
            StackName='data-protection-cse',
            TemplateURL='https://s3.amazonaws.com/crypto-workshop-dont-delete/template-cse.yaml',
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ],
        )
        
    # client side encryption with data key caching
    try:
        response = client.describe_stacks(
            StackName='data-protection-cse-datakey-caching',
        )
    except:
        response = client.create_stack(
            StackName='data-protection-cse-datakey-caching',
            TemplateURL='https://s3.amazonaws.com/crypto-workshop-dont-delete/template-cse-data-key-caching.yaml',
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ],
        )
        
    # acm pca private certs for domains 
    try:
        response = client.describe_stacks(
            StackName='acm-pca-usecase-6',
        )
    except:
        response = client.create_stack(
            StackName='acm-pca-usecase-6',
            TemplateURL='https://s3.amazonaws.com/crypto-workshop-dont-delete/acm-alb-pca.yaml',
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ],
        )
        
    print "All cloudformation stacks have been setup for the workshops"
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)