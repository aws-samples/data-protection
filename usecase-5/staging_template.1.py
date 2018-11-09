"""
#####################################################################################
#                                                                                   #
#   Using curl command to succesfully authenticate webserver over a TLS connection  #
#   This is a very simple web app that prints hello world                           #
#                                                                                   #
#####################################################################################
"""
import os
import sys 

def main():
    """
    ######################################################################################
    #                                                                                    #
    #   1.Runing curl to hit the website                                                 #
    #                                                                                    #
    #   2.You will see in the run configuration window that this line gets printed :     #
    #                                                                                    #
    #   Hello World !!                                                                   #
    #                                                                                    #
    ######################################################################################
    """
    try:
        CURRENT_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
        curl_command = 'curl --verbose --cacert ' + CURRENT_DIRECTORY_PATH + 'webserver_cert_chain.pem ' + \
                  '-X GET https://127.0.0.1:5000/'
        os.system(curl_command)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    