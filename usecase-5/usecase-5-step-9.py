#####################################################################################
#                                                                                   #
#   Using curl command to succesfully authenticate webserver over a TLS connection  #
#   This is a very simple web app that prints hello world                           #
#                                                                                   #
#####################################################################################

import boto3
import sys 
import os 

try:
    current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    curl_command = 'curl --verbose --cacert ' + current_directory_path + 'webserver_cert_chain.pem ' + \
                  '-X GET https://127.0.0.1:5000/'
    os.system(curl_command)
    dbg = 'Stop' 
    ######################################################################################
    #                                                                                    #
    #   1.Runing curl to hit the website                                                 #
    #                                                                                    #
    #   2.You will see in the run configuration window that this line gets printed :     #
    #                                                                                    #
    #   SSL connection using TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384                       #
    #                                                                                    #
    ######################################################################################
    
except SystemExit as e:
    exit(0)    
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)
 
