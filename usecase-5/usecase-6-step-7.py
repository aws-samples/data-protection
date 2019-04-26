"""
################################################################
#   Using curl command to authenticate the private domain      #
#   https://alb.workshop.com over a TLS connection             #
#   This is a very simple web app that prints hello world      #
################################################################
"""
import os
import sys 
import subprocess
import shlex

def main():
    """
    ######################################################################################
    #   1.Runing curl to hit the private domain https://alb.workshop.com                 #
    #                                                                                    #
    #   2.You will see in the run configuration window that this line gets printed :     #
    #   curl: (60) Peer's Certificate issuer is not recognized. Why did this happen ?    #
    ######################################################################################
    """
    try:
        command = "curl --verbose https://alb.workshop.com"
        command = shlex.split(command)

        returned_output = subprocess.check_output(command)
        print returned_output
        print "\nStep-7 has been successfully completed \n"
    except subprocess.CalledProcessError as e:
        print "\nCertificate is not trusted - cannot validate server certificate"
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)
        
if __name__ == "__main__":
    main()
    