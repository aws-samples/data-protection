# Templates :

## Overview
In this section, we will learn about certificate extensions that can help you use certificates for applications beyond the common ubiquitous case of identifying TLS server endpoints. These include 

* Code signing
* Signing Online Certificate Status Protocol (OCSP) responses
* ADCS certificates

What makes one certificate useful for signing code and another useful for terminating TLS are the various fields and extensions in the certificate. Extension fields, or simply extensions, define the usage of the certificate. There are a few extensions defined in RFC 5280 that are commonly used and broadly supported, including 

* **Basic Constraints**
* **Key Usage**
* **Extended Key Usage**

ACM Private CA provides complete flexibility in generating various kinds of certificates using four varities of templates :

* Base template
* CSRPassthrough templates
* APIPassthrough templates
* APICSRPassthrough templates

In this usecase, you will learn how different certificate types can be issued by using the different template types that are available :

## Default template example :

In this exercise, you will create a code signing certificate using the pre-built templates provided by ACM Private CA.

Ensure you have run the "environment-setup.sh" script under usecase-9 folder in Cloud9 as AppDev role.

Follow these steps by right clicking and opening this link : [Template ACM Private CA](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/TemplateCodeSigning.pdf)


## Blank template example :

ACM Private CA provides a blank template where you can control certificate parameters or extensions by using CSR passthrough or API passthrough. The blank template is useful if you need complete customization of certifcates, such as building email certificates, smartcard logon certificates or any others where you need to fully control certificate parameters or extensions. We will be using the [issuecertificate](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Client.issue_certificate) API call.


### Email Certificates

In this example, we will see how to use Blank templates to generate email S/MIME certificates using the *BlankEndEntityCertificate_APIPassthrough/V1* template. But first what is an email certificate?

Email certificates use the [S/MIME (Secure/Multipurpose Internet Mail Extensions) standard](https://tools.ietf.org/html/rfc3850). The main purposes of S/MIME certificates are:
* Authentication / Message integrity
* Data security (encryption)
Keep in mind, while we are splitting out the signing and encryption email certificates, you can create a single certificate for both. 

#### Email Signing Certificate
This S/MIME certificate verifies the email sender's identity for the recipient. More generally, it allows users to digitally sign their emails to verify their identity through the attestation of a trusted third party known as a certificate authority (CA).

Follow these steps by right clicking and opening this link : [Email Signing Certificate Creation - ACM Private CA](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/EmailCertSigning.pdf)

#### Email Encryption Certificate
This S/MIME certificate encrypts the actual content being sent via email. More generally, it allows users to encrypt the entire contents (messages, attachments, etc.) of their emails so that the information is secure before it transmits from server to server across the internet. This helps to protect the data from man-in-the-middle (MitM) attacks.

Follow these steps by right clicking and opening this link : [Email Encryption Certificate Creation - ACM Private CA](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/EmailEncrypt.pdf)

#### Takeaways
Notice that with Email Signing Certificate the KeyUsage is 'DigitalSignature' and 'NonRepudiation'. This makes sense because we are protecting concerned with authentication and message integrity. 

With Email Encryption Certificate the KeyUsage is 'KeyEncipherment' since we are encrypting the contents of the email. 

Please take this [Quiz](https://amazonmr.au1.qualtrics.com/jfe/form/SV_5w05YCIznyp80bc) to enhance your learning.

#### Conclusion
As you can see this created two .pem files with the contents of the certificates. The first certificate is for S/MIME Signing and the second is for S/MIME Encryption. Keep in mind you can combine them into one certificate if needed, however some organizations split these up so that if one is not available, employees can still send signed, unencrypted emails. Some email client will require you to convert it to [PKCS12 format](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization.html?highlight=pkcs12#cryptography.hazmat.primitives.serialization.pkcs12.serialize_key_and_certificates).






