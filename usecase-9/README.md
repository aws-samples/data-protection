# ACM Private Certificate Authority (ACM Private CA) Workshop 

This workshop demonstrates how ACM Private Certificate Authority (PCA) makes it easy for managing your PKI infrastructure and generating private certificates for TLS terminations on web servers and IOT devices. You will get hands on experience on the following use cases :

* Creating a complete Certificate Authority(CA) hierarchy 
* Creating a private certificate and putting it on an HTTPS listener of an application load balancer(ALB) that will terminate TLS. The client connection will come from a browser of your choice.
* Using private certificates on IOT devices so that the IOT devices can authenticate with AWS IOT Core and exchange messages
* Learn how to monitor security events associated with your private Certificate Authority using Cloudwatch and Security Hub
* Learn Security best practices for your PKI infrastructure
* Using certificate templates for generating different certificate types such as code signing, S/MIME email certificates, smart card logon and others.
* Throughout the workshop theare are multiple quizzes for re:inforced learning

### 1.A If you are using a AWS provided account for this workshop (at an AWS event)

* If you are logged into your personal AWS account or your corporate AWS account, you should log out now.
* Open this link in a new browser tab: [AWS provided account](https://dashboard.eventengine.run/)
* Log in with your hash that's provided to you during the event
* Click on the **AWS Console** button
* It should bring up a pop-up screen. On the pop-up,  under Login Link click on **Open Console**
* You should be logged into the AWS provided account
* Please verify that the region with staff running the evet

### 1.B If you are using your own AWS account

* Log into your desired AWS account
* You should be logged into the AWS provided account
* Please verify that you're in the desired region. Please use a AWS region in which AWS Cloud9 and AWS Certificate Managed(ACM) service is available. You can find the supported reqions for a service here : [Supported Regions for services](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/)
* To avoid any permissions issues in your account, please make sure that you have administrator access. Also S3 block public access needs to be disabled for the CRL S3 buckets so that these buckets are accessible by the TLS client.
* Please download the CF template by right clicking this link: [Security Admin Cloudfromation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-9/cf-templates/template-security-admin.yaml) and save link as the filename **template-security-admin.yaml**
* Upload and launch the cloudformation stack in the AWS account that you are logged into. If you are not familiar with this, follow instructions here by right clicking and opening this link [Deploy Security Admin Cloudformation Stack Instructions](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/SecurityAdminSteps.pdf) in a new browser tab Deploy Security Admin Cloudformation Stack Instructions

## Quizzes

During the AWS Certificate Management Private CA Workshop you will have the opportunity to take multiple quizzes. To do that, we have embedded quiz links throughout the workshop. We're hoping that you'll take 2 minutes of your time per quiz. This will enhance learning and allow us to hold a discussion during the workshop.
This quiz is hosted by an external company (Qualtrics), so the link above does not lead to our website. Please note that AWS will own the data gathered via this quiz, and will not share the information/results collected with quiz respondents. AWS handles your information as described in the [AWS Privacy Notice](https://aws.amazon.com/privacy/).

## Let's setup the Certificate Authority Hierarchy 

### 2. An IAM Role called **CaAdminRole** is the role that a CA administrator would assume. 

* Assume the role named **CaAdminRole** by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Certificate Authority administrator will need for CA administration. As a CA administrator, you will be responsible for creating a root and subordinate certificate authority 

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/SwitchRole.pdf)

### 3. Create Private CA hierarchy
You can create Private Root and Subordinate Certificate Authorities either manually (See section 3.A) or through CloudFormation template (See Section 3.B). Please choose the manual or the Cloudformation option but don't do both.

#### 3.A - Create Private CA Hierarch Manually 

###### 3.A.1 Build the S3 bucket needed for storing CRL's(Certificate revocation lists) by deploying the cloudformation template below

To create S3 bucket that will contain the certificate revocation list (CRL), please download the CF template by right clicking and save link as the filename *template-ca-admin.yaml* [CA Admin Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-9/cf-templates/template-ca-admin.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in the AWS account that you are logged into. If you are not familiar with this, follow instructions here by right clickking and opening link in a new browser tab [Deploy CA Admin Cloudformation Stack Instructions](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/CAAdminSteps-1.pdf)

###### 3.A.2 Create a Root CA. 

* Navigate to ACM Service in the AWS Console
* Click Get Started under Private Certificate Authority
* Open this link in a new browser tab for the rest of the steps : [Creating a Root CA](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/Root%20CA%20Creation-1.pdf)

###### 3.A.3 Root CA Quiz Time (Open in new tab)
[Quiz 1](https://bit.ly/2To8mmf)

[Quiz 2](https://bit.ly/2YQr7El)

###### 3.A.4 Create a Subordinate Issuing CA. 

* Navigate to ACM Service in the AWS Console
* Under Private CA's, click on the **Create CA** button
* Open this link in a new browser tab for the rest of the steps  : [Creating a Subordinate CA](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/SubordinateCACreation.pdf)

#### 3.B - Create full Private CA Hierarch automatically with a CloudFormation Template 

Please download the CF template by right clicking and save link as the filename *template-pca-hierarchy.yaml* [PCA Hierarchy CF template](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-9/cf-templates/template-pca-hierarchy.yaml)
Upload and launch the cloudformation stack in the AWS account that you are logged into. If you are not familiar with this, follow instructions here by right clickking and opening link in a new browser tab [Deploy CA Admin Cloudformation Stack Instructions](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/CAAdminSteps-1.pdf)

### 4. Quiz time. Open this link in a new browser tab: [quiz](https://bit.ly/2yQ5IML)

## Sections :

You can choose any of the sections in the table below.

| Section    | Average time to complete section |
| :------------- |:-------------|
| [Using Private Certificates on a HTTPS Web Application ](https://github.com/aws-samples/data-protection/blob/master/usecase-9/HTTPS_Application_Usecase.md)  | 35 mins| 
| [Monitoring ACM Private CA ](https://github.com/aws-samples/data-protection/blob/master/usecase-9/Monitoring_ACM_Private_CA.md)  | 35 mins| 
| [Creating different certificate types using Certificate Templates](https://github.com/aws-samples/data-protection/blob/master/usecase-9/Templates_ACM_Private_CA.md)  | 20 mins| 

If you have extra time after finishing the above use cases, please continue with the below use case on IOT. This section is optional

| Section    | Average time to complete section |
| :------------- |:-------------|
| [Private Certificates for IOT Devices ](https://github.com/aws-samples/data-protection/blob/master/usecase-9/IOT_Device_Usecase.md)  | 45 mins| 

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.

[LICENSE](LICENSE)

## Cleanup

#### If you are at an AWS physical or virtual event

Don't worry about cleanup, we will take care of it. Hopefully you've learned something useful in this workshop that you can take back your organization. Thank you for coming.

#### If you are doing this workshop on your own

Please delete all the Certificate authorities and the certificates that you have created so that you are not billed.

#### License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.

