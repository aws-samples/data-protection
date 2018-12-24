#######################################
#     Initial environment setup       #
#######################################

import sys 
import os 
import subprocess

try:
    print subprocess.check_output(['sudo','pip','install','boto3'])
    print subprocess.check_output(['sudo','pip','install','aws-encryption-sdk'])
    print subprocess.check_output(['sudo','pip','install','ikpdb'])
    print subprocess.check_output(['sudo','pip','install','pathlib'])
    print subprocess.check_output(['sudo','pip','install','flask'])
    print subprocess.check_output(['sudo','pip','install','pyopenssl'])
    print "\n"
    print "Workshop environment setup was successful"
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)