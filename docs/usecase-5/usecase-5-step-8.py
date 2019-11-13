"""
################################################################
#   Making http to authenticate the private domain             #
#   https://alb.workshop.com over a TLS connection             #
#   This is a very simple web app that prints hello world      #
################################################################
"""
import os
import requests

def main():
    """
    ##############################################################################
    #   1.Issue get request to private domain https://alb.workshop.com           #
    #   2.You will see the html returned in the response                         #
    ##############################################################################
    """

    cwd = os.getcwd()
    try:
        self_signed_cert_file = cwd+'/data-protection/usecase-5/self-signed-cert.pem'
        # what happens if self_signed_cert_file=False?
        response = requests.get('https://alb.workshop.com', verify=self_signed_cert_file)
        print(response.text)
        print("\nCertificate is trusted and is valid")
        print("\nStep-8 has been successfully completed \n")
        exit(0)
    except requests.exceptions.RequestException as e:
        print('Exception:',e)
        exit(1)


if __name__ == "__main__":
    main()
    