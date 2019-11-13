# AWS Data Protection Workshops

If you are considering protecting data in your [AWS](https://aws.amazon.com/) environment using methods such as encryption or certificate management, these workshops can help you learn in depth. We will be using the [Cloud9 IDE environment](https://aws.amazon.com/cloud9/) and a combination of [Python](https://www.python.org/) code and AWS console access for these workshops.

# Ubiquitous Encryption 

Data encryption provides a strong layer of security to protect data that you store within AWS services. AWS services can help you achieve ubiquitous encryption 
for data in transit as well as data at rest.

<a><img src="./images/ubiquitous-encryption.png" width="989" height="557"></a>

# Workshops

These workshops demonstrates server side encryption, client side encryption and certfificate management concepts within AWS. For example :

| Title | Description | Learning Time | Teaching Time With Discussion | 
| :------- | :---------- | :-- | :-- |
| [Level 200: Server Side Encryption](./usecase-1/)  | This workshop demonstrates server side encryption on S3 | 15 min | 30 min |
| [Level 200: Client Side Encryption](./usecase-2/)  | This workshop demonstrates client side encryption | 15 min | 30 min |
| [Level 200: Client Side Encryption With Data Key Caching](./usecase-3/)  | This workshop demonstrates client side encryption with data key caching | 15 min | 30 min |
| [Level 300: Creating Private Certs ACM Private Certificate Authority - Mode-1 ](./usecase-4/)  | This workshop demonstrates how you create a AWS Certificate Manager private certificate authority(PCA) and use ACM PCA to sign a CSR to create a private certificate | 40 mins | 1 hour |
| [Level 300: Creating Private Certs ACM Private Certificate Authority - Mode-2 ](./usecase-5/)  | This workshop demonstrates how you create a AWS Certificate Manager private certificate authority and use this CA to create private X.509 certififcates for a private domain | 40 mins | 1 hour |
| [Level 300: Creating a complete private CA hierarchy on AWS ](./usecase-6/)  | This workshop demonstrates how you create a AWS Certificate Manager private certificate authority and use this CA to create private X.509 certififcates for a private domain and apply the cert on an application load balancer | 1 hour | 1 hour 30 mins |
| [Level 300: ACM Private CA Best Practices, Monitoring and Templates for code signing certificates ](./usecase-7/)  | This workshop demonstrates private CA best practices, monitoring and use of templates for code siging certs|1 hour 30 mins | 2 hours |
| [Level 300: KMS Managed keys and ACM Private CA best practices combo workshop](./usecase-8/)  | This workshop demonstrates to use KMS with AWS managed keys and completing a complete CA hiearchy on AWS | 1 hour 40 mins | 1 hour |

### Region Support

Since these workshops use the Cloud9 IDE, you can use run these workshops in the following regions where the AWS Cloud9 
service is available : 
* **N.Virginia** (us-east-1)
* **Ohio** (us-east-2)
* **Oregon** (us-west-2)
* **Ireland** (eu-west-1)
* **Singapore** (ap-southeast-1)

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.


