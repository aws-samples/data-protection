## KMS and ACM Private Certificate Authority (ACM Private CA) Workshop

This workshop has two parts :

1.First part demonstrates how you can use KMS with S3 for server side encryption while storing objects on S3. Different encryption options and separation of duties between a key administrator and key user is also explored.
2.The second part is about how ACM Private Certificate Authority (PCA) service can be used to create a complete CA hierarchy, generate a private certificate, and apply the private certificate on an Application Load Balancer while following security best practices.

### You will be using a AWS provided account for this workshop :

* If you are logged into your personal AWS account or your corporate AWS account, you should log out now.
* Open this link in a new browser tab: [AWS provided account](https://dashboard.eventengine.run/)
* Log in with your hash provided on the piece of paper which says **Event Engine Hash**
* Click on the **AWS Console** button
* It should bring up a pop-up screen. On the pop-up,  under Login Link click on **Open Console**
* You should be logged into the AWS provided account
* Please verify that the region selected is **Ireland**

### Part 1 : Using KMS for encrypting data on AWS services

As a first step, please download this file to your laptop by **right clicking** the below link and save link as the filename *to_upload.txt* to any folder on your laptop

[Download File](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-8/files/to_upload.txt) 

This workshops will cover two scenarios :

#### AWS Managed Keys :

Server side encryption on S3 using **AWS Managed Keys**

For instructions, right click and open this link in a new browser tab : [Click here for instructions](https://view.highspot.com/viewer/5d9e69b634d6be6992300ade)

Let's work on a quiz on this topic :

Quiz : [quiz](https://bit.ly/2BcatBk)

#### Customer Managed Keys(CMK) :

Server side encryption on S3 using **Customer Managed Keys** with separation of duties between key administrators and key users.

For instructions, right click and open this link in a new browser tab : [Click here for instructions](https://view.highspot.com/viewer/5d9e6e10f7794d2efc187cbe)

Let's work on a quiz on this topic :

Quiz: [quiz](https://amazonmr.au1.qualtrics.com/jfe/form/SV_eXNtTUFRCopu48R)

### Part 2 : Create a complete CA hierarchy using ACM Private CA and deploying private certificates

#### 1. An IAM Role called **CaAdminRole** is the role that a CA administrator would assume. 

* Assume the role named CaAdminRole by using switch role on the AWS console in the AWS account that you are currently logged into. The role name is **case sensitive**

* This role has permissions that a Certificate Authority administrator will need for CA administration. As a CA administrator you will be responsible for creating a root and subordinate certificate authority
hierarchy

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://view.highspot.com/viewer/5d66bc5cc79c523342504c3e)

#### 2. Build the infrastructure needed for creating a CA hierarchy by deploying the cloudformation template below

Please download the CF template by **right clicking** and save link as the filename *template-ca-admin.yaml* [CA Admin Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-6/cf-templates/template-ca-admin.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in the AWS account that you are logged into. If you are not familiar with this, follow instructions here by right clickking and opening link in a new browser tab [Deploy Cloudformation Stack Instructions](https://view.highspot.com/viewer/5d65968f81171753be07bd54)

#### 3. Create a Root CA. 

* Navigate to ACM Service in the AWS Console
* Click Get Started under Private Certificate Authority
* Open this link in a new browser tab for the rest of the steps : [Creating a Root CA](https://view.highspot.com/viewer/5d5b129b6a3b116f4230f242)

#### 4. Create a Subordinate Issuing CA. 

* Navigate to ACM Service in the AWS Console
* Under Private CA's click on the **Create CA** button
* Open this link in a new browser tab for the rest of the steps  : [Creating a Subordinate CA](https://view.highspot.com/viewer/5d9e91c1a2e3a9148b6d7deb)

#### 5. Quiz time. Open this link in a new browser tab : [quiz](https://bit.ly/2yQ5IML)

#### 6. An IAM Role called **AppDevRole** is the role that an application developer would assume. 

* Assume the role named **AppDevRole** by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Application developer will need for building an web aplication which is fronted by an application load balancer and behind the load balancer is a lambda origin that
provides the HTML code for a website. The application developer will also have permissions to issue a certificate under a certificate authority that they select.

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://view.highspot.com/viewer/5d66bc5cc79c523342504c3e)

#### 7. Build the application infrastructure by deploying the cloudformation template below

Please download the CF template by **right clicking** and save link as the filename *template-appdev.yaml* [AppDev Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-6/cf-templates/template-app-dev.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. If you are not familiar with this, follow instructions here by right clicking and opening link in a new browser tab [Deploy Cloudformation Stack Instructions](https://view.highspot.com/viewer/5d65968f81171753be07bd54)
This cloudformation deployment takes about 3 minutes to complete.

#### 8. Next step is to issue a private certificate to put on the application load balancer. 

Open this link in a new browser tab for steps : [Issue a private certificate](https://view.highspot.com/viewer/5d5b133d6a3b116f29313a10)  

#### 9. Attach a HTTPS listener and private certificate to the ALB . 

Open this link in a new browser tab for steps : [Attach HTTPS Listener](https://view.highspot.com/viewer/5d669c21628ba22ca196b49e)  

#### 10. Validate the identity of the ALB with the browser that your are using. Please open link in a new browser tab

For firefox : [Validate Certificate Identity on Firefox broswer](https://view.highspot.com/viewer/5d5c1fe23f65f635ae005a47)  

For google chrome : [Validate Certificate Identity on chrome browser](https://view.highspot.com/viewer/5d5c42da66bbaa2fc928a575)

For Microsoft Edge : [Validate Certificate Identity on Microsoft edge browser](https://view.highspot.com/viewer/5d5c2e5cf7794d4833e8207a)

#### 11. Quiz time. Open this link in a new browser tab : [quiz](https://bit.ly/2Zh3iRY)

#### 12. Cleanup

Don't worry about cleanup, we will take care of it. Hopefully you learnt something useful in this workshop that you can take back your organization. Thank you for coming.

### License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
