# AWS Data Protection Workshops

If you are considering protecting data at rest and in transit within your [AWS](https://aws.amazon.com/) environments using methods such as encryption or certificate management, these workshops can help you learn in depth.

# Ubiquitous Encryption 

Data encryption provides a strong layer of security to protect data that you store within AWS services. AWS services can help you achieve ubiquitous encryption 
for data in transit as well as data at rest.

<a><img src="images/ubiquitous-encryption.png" width="989" height="557"></a>

# Workshops

| Title | Description | Learning Time | Teaching Time With Discussion | 
| :------- | :---------- | :-- | :-- |
| [Level 200: Server Side Encryption](usecase-1/)  | This workshop demonstrates server side encryption on S3 using a boto3 python script | 15 min | 30 min |
| [Level 200: Client Side Encryption](usecase-2/)  | This workshop demonstrates client side encryption using a master key materials provider and python encryption SDK | 15 min | 30 min |
| [Level 200: Client Side Encryption With Data Key Caching](usecase-3/)  | This workshop demonstrates client side encryption with data key caching using the python encryption sdk | 15 min | 30 min |
| [Level 300: Creating Private Certs ACM Private Certificate Authority - Mode-1 ](usecase-4/)  | This workshop demonstrates how you create a AWS Certificate Manager private certificate authority(PCA) and use ACM PCA to sign a CSR to create a private certificate | 40 mins | 1 hour |
| [Level 300: Creating Private Certs ACM Private Certificate Authority - Mode-2 ](usecase-5/)  | This workshop demonstrates how you create a AWS Certificate Manager private certificate authority and use this CA to create private X.509 certififcates for a private domain and apply the cert on an application load balancer | 40 mins | 1 hour |

**NOTE:** The ACM PCA use cases (the latter 2) can only be run within the VPC where the ALB is deployed as a private DNS name space is used. This will work within the Cloud9 IDE but not from machines that are outside of the VPC. 

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.


