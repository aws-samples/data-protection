# AWS Encryption & Certificate Management Workshops

If you are dealing with data encryption or certificate management within your AWS account, these workshops can help. This workshop is based on python programming language and uses the AWS Cloud9 IDE

# Ubiquitous Encryption 

To ensure that data is encrypted within your AWS architecture  AWS provides various tooling to achieve ubiquitous encryption 
for data in transit as well as datat at rest

![Components](images/ubiquitous-encryption.png)

## Workshops

> Please review and complete all prerequisites before attempting these workshops.

Title               | Description
:---: | :---
[Key admins And Key Access](./aws-kms-key-policy/)  | This workshop demonstrates how KMS key policies works for admins and users
[Server Side Encryption](https://git-codecommit.us-east-1.amazonaws.com/v1/repos/cryptobuilders/kms-sse-usecase-1/)  | This workshop demonstrates how you can use boto3 and python to demonstrate AWS Server side encryption 
[Client Side Encryption](./aws-kms-client-side-encryption/)  | This workshop demonstrates how you can use boto3 and python to demonstrate AWS client side encryption 
[Client Side Encryption With Data Key Caching](./aws-kms-client-side-encryption-data-key-caching/)  | This workshop demonstrates how you can use boto3 and python to demonstrate AWS client side encryption with data key caching
[Creating Certs With ACM Private Certificate Authority](./aws-acm-private-certificate-authority/)  | This workshop demonstrates how you can use boto3 and python to create a AWS Certificate Manager private certificate authority and use this CA to create private X.509 certififcates
## Prerequisites

### AWS Account

In order to complete these workshops you'll need a valid, usable AWS Account with Admin permissions.  The code and instructions in these workshops assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you'll run into naming conflicts for certain resources. 

Use a **personal account** or create a new AWS account to ensure you have the neccessary access. This should not be an AWS account from the company you work for.

All of the resources you will launch as part of these workshops are eligible for the AWS free tier if your account is less than 12 months old. See the [AWS Free Tier](https://aws.amazon.com/free/) page for more details.  If you are doing this workshop as part of an AWS sponsored event, you will receive credits to cover the costs.

### Cloudformation templates for initial environment setup

Please run these cloudformation stacks in your AWS account as this is required for all the workshops

[![Deploy IAM user creation stack](images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=cryptobuilders-iam-user-creation&templateURL=https://s3.amazonaws.com/crypto-builders-cf-templates/template-create-user.yaml)

The above stack creates an IAM user called **builders-session-user** .Before you launch the next stack please login into your account as the **builders-session-user**

[![Deploy IAM user creation stack](images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=cryptobuilders-env-setup&templateURL=https://s3.amazonaws.com/crypto-builders-cf-templates/template-env-setup.yaml)

The above stack creates an Cloud9 IDE environment called **crypto-builders** .Before you launch the next stack please login into your account as the **builders-session-user**


### Browser

These workshops assume you are using a Cloud IDE environment. We recommend you use the latest version of Chrome or Firefox to complete this workshop.

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
