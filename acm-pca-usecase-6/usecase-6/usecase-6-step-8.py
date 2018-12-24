"""
#####################################################################################
#                                                                                   #
#   Using curl command to succesfully authenticate the private domain               #
#   alb.workshop.com over a TLS connection                                          #
#   This is a very simple web app that prints hello world                           #
#                                                                                   #
#####################################################################################
"""
import os
import sys 
import subprocess
import shlex

def main():
    """
    ##############################################################################
    #                                                                            #
    #   1.Runing curl to hit the private domain https://alb.workshop.com         #
    #                                                                            #
    #   2.You will see in the runner pane window that the following lines        #
    #     gets printed                                                           #
    #                                                                            #
    #   Hello World !!                                                           #
    #                                                                            #
    ##############################################################################
    """
    try:
        CURRENT_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
        command = 'curl --verbose --cacert ' + CURRENT_DIRECTORY_PATH + 'cert_chain.pem ' + \
                  'https://alb.workshop.com'
        command = shlex.split(command)
        returned_output = subprocess.check_output(command)
        print returned_output
        print "Certificate is trusted and is valid"
    except subprocess.CalledProcessError as e:
        print "\nCertificate is not trusted - cannot validate server certificate"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    