"""
##########################################################################################
# Create a subordinate private certificate authority(CA) using AWS Certfificate Manager  #
##########################################################################################
"""
import os
import subprocess
import sys
import random
import json
import boto3

def main():
    """
    #########################################################################################
    #  Create a CRL S3 bucket and a subordinate private certificate authority(CA) using ACM #
    #########################################################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        
if __name__ == "__main__":
    main()
    