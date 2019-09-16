"""
################################################################
#   Making http to authenticate the private domain             #
#   https://alb.workshop.com over a TLS connection             #
#   This is a very simple web app that prints hello world      #
################################################################
"""
import requests

def main():
    """
    #############################################################################
    #   1.Issue get request to private domain https://alb.workshop.com          #
    #   2.You will see the error message of the exception - what happened?      #
    #############################################################################
    """
    try:
        response = requests.get('https://alb.workshop.com')
        exit(1)
    except requests.exceptions.RequestException as e:
        print('Exception:',e)
        print("\nCertificate is not trusted - cannot validate server certificate")
        print("\nStep-7 has been successfully completed \n")
        exit(0)

if __name__ == "__main__":
    main()
    