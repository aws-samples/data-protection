###########################################################################
#                                                                         #
#   Run a web server using the python flask moduke                        #
#   this is a very simple web app that prints hello world                 #
#                                                                         #
###########################################################################

import boto3
import sys 
import os 
from flask import Flask

try:
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "\nHello World!\n\n"
    
    if __name__ == "__main__":
        #app.run(ssl_context='adhoc')
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        webserver_cert_path = current_directory_path + 'webserver_cert.pem'
        webserver_key_path = current_directory_path + 'webserver_privkey.pem'
        app.run(ssl_context=(webserver_cert_path, webserver_key_path))
    
    dbg = 'Stop' 
    ##################################################################################################
    #   Runing a flask web server                                                                  #
    #                                                                                                #                                                                                            
    #   This is a simple web app that prints hello world                                           #                           #
    #                                                                                                #
    #   The web server endpoint cert  file is called webserver_cert.pem                            #
    #                                                                                                #
    #   The certificate chain file is called webserver_cert_chain.pem                              #
    #                                                                                                #
    #   In your terminal make sure that you are in the directory AWS-Certificate-Manager/usecase-1 #
    #                                                                                                #
    #   We will use the following curl command line statement to verify whether TLS                #
    #     authentication was successful.                                                             #
    #                                                                                                #
    #     curl --verbose --cacert webserver_cert_chain.pem -X GET https://127.0.0.1:5000/            #
    #                                                                                                #
    #   7.Once you execute the above curl command you will see hello world printed                   #
    ##################################################################################################
    
except SystemExit as e:
    exit(0)    
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)
 
