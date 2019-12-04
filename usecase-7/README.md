# ACM Private Certificate Authority (ACM Private CA)

This workshop demonstrates how ACM Private Certificate Authority (PCA) service can be used to create a complete CA hierarchy, generate a private certificate, and apply the 
private certificate on an Application Load Balancer while following security best practices.

#### 1. You will be using a AWS provided account for this workshop.

* If you are logged into your personal AWS account or your corporate AWS account, you should log out now.
* Open this link in a new browser tab: [AWS provided account](https://dashboard.eventengine.run/)
* Log in with your hash
* Click on the **AWS Console** button
* It should bring up a pop-up screen. On the pop-up,  under Login Link click on **Open Console**
* You should be logged into the AWS provided account
* Please verify that the region selected is **Oregon**

## Setup Certificate Authority Hierarchy 
#### 2. An IAM Role called **CaAdminRole** is the role that a CA administrator would assume. 

* Assume the role named CaAdminRole by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Certificate Authority administrator will need for CA administration. As a CA administrator you will be responsible for creating a root and subordinate certificate authority
hierarchy

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://view.highspot.com/viewer/5d66bc5cc79c523342504c3e)

#### 3. Build the infrastructure needed for creating a CA hierarchy by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-ca-admin.yaml* [CA Admin Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-7/cf-templates/template-ca-admin.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in the AWS account that you are logged into. If you are not familiar with this, follow instructions here by right clickking and opening link in a new browser tab [Deploy CA Admin Cloudformation Stack Instructions](https://view.highspot.com/viewer/5dd6cd89a2e3a96cb78647d3)

#### 4. Create a Root CA. 

* Navigate to ACM Service in the AWS Console
* Click Get Started under Private Certificate Authority
* Open this link in a new browser tab for the rest of the steps : [Creating a Root CA](https://view.highspot.com/viewer/5d5b129b6a3b116f4230f242)

#### 5. Create a Subordinate Issuing CA. 

* Navigate to ACM Service in the AWS Console
* Under Private CA's click on the **Create CA** button
* Open this link in a new browser tab for the rest of the steps  : [Creating a Subordinate CA](https://view.highspot.com/viewer/5d9e91c1a2e3a9148b6d7deb)

#### 6. Quiz time. Open this link in a new browser tab: [quiz](https://bit.ly/2yQ5IML)

## Create Application

#### 7. An IAM Role called **AppDevRole** is the role that an application developer would assume. 

* Assume the role named **AppDevRole** by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Application developer will need for building an web aplication which is fronted by an application load balancer and behind the load balancer is a lambda origin that
provides the HTML code for a website. The application developer will also have permissions to issue a certificate under a certificate authority that they select.

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://view.highspot.com/viewer/5d66bc5cc79c523342504c3e)

#### 8. Build the application infrastructure by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-appdev.yaml* [AppDev Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-7/cf-templates/template-app-dev.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. If you are not familiar with this, follow instructions here by right clicking and opening link in a new browser tab [Deploy AppDev Cloudformation Stack Instructions](https://view.highspot.com/viewer/5dd6cd3c6a3b1102db4ac3ca)
This cloudformation deployment takes about 3 minutes to complete.

#### 9. Next step is to issue a private certificate to put on the application load balancer. 

Open this link in a new browser tab for steps : [Issue a private certificate](https://view.highspot.com/viewer/5d5b133d6a3b116f29313a10)  

#### 10. Attach a HTTPS listener and private certificate to the ALB. 

Open this link in a new browser tab for steps : [Attach HTTPS Listener](https://view.highspot.com/viewer/5d669c21628ba22ca196b49e)  

#### 11. Validate the identity of the ALB with the browser that your are using. Please open link in a new browser tab

For Firefox: [Validate Certificate Identity on Firefox Browser](https://view.highspot.com/viewer/5d5c1fe23f65f635ae005a47)  

For Google Chrome: [Validate Certificate Identity on Chrome Browser](https://view.highspot.com/viewer/5d5c42da66bbaa2fc928a575)

For Microsoft Edge: [Validate Certificate Identity on Microsoft Edge Browser](https://view.highspot.com/viewer/5d5c2e5cf7794d4833e8207a)

For Google Chrome on Windows: [Validate Certificate Identity on Windows](https://view.highspot.com/viewer/5dcadc15b7b739360b417fb5)

#### 12. Quiz time. Open this link in a new browser tab: [quiz](https://bit.ly/2Zh3iRY)

#### 13. Cloud9 IDE environment setup

* Navigate to the Cloud9 service within your AWS console
* Open the Cloud9 IDE environment called **workshop-environment**. It takes about 30 seconds for the environment to start up.
* In the Cloud9 IDE environment you will find a folder called data-protection in the folder pane on the left side of the screen
* Right-click (on MacOS: control-click) the file named environment-setup.sh in the IDE and select Run
* This script takes about a minute to complete
* In the runner window below you should see **SUCCESS: installed python dependencies ** followed by a list of the installed packages

## Security Monitoring:

In this section we will look at how to monitor privileged actions as you build your certificate management infrastructure. We will study two scenerios. The creation of a CA Certificate and mass revocation of end entity certificates. 

#### 14. [Scenerio 1]: Monitor Mass Revocation
This scenerio shows a developer revoking many end-entity certificates within a short period of time. We want to monitor and notify the security team if this type of privileged action takes place in order to investigate.

##### 15. Create/Revoke End-Entity Certificates
First we will act as the Developer by creating and then revoking many certificates at once: [Mass revocation](https://view.highspot.com/viewer/5da634e266bbaa2860b471a7)

##### 16. Quiz time. Open this link in a new browser tab : [quiz](https://amazonmr.au1.qualtrics.com/jfe/form/SV_3mHHKwvVlxQ0v1X)

##### 17. Mass Revocation Alarm Setup
Setup CloudWatch Alarms: [Revocation Alarm setup](https://view.highspot.com/viewer/5da6342834d6be298b1c4447)

#### 18. [Scenerio 2]: CA Certificate Created
Creating a CA Certificate is a privileged action that should only be taken by authorized personnel within the CA Hierarchy Management team. For this reason we want to monitor the creation of any CA Certificate within our hierarchy. 

To do this we will setup a CloudWatch Alarm: [CA Cert Alarm setup](https://view.highspot.com/viewer/5da63481b7b73956e4842f3a)

#### 19. Quiz time. Open this link in a new browser tab : [quiz](https://amazonmr.au1.qualtrics.com/jfe/form/SV_cx0KvGMDSVUVLTL)

#### 20. Create Dashboard
Now we have two alarms that have produced ALARM states. This is due to our mass revocation of multiple certificates by the application developer and the creation of a CA Certificate upon creating our CA hierarchy. Organizations can use this mechanism to build dashboards to monitor and alert (SNS, Email, etc) when sensitive actions take place.

Create CloudWatch Dashboard: [Create Dashboard](https://view.highspot.com/viewer/5dc592fba4dfa00d2cbd64c6)

## Advanced Section :

In this section we will learn about certificate extensions that can help you use certificates for applications beyond the common case of identifying TLS server endpoints. These include 

* code signing
* signing Online Certificate Status Protocol (OCSP) responses
* TLS clients for two-way (mutual) authentication

What makes one certificate useful for signing code and another useful for terminating TLS are the extension fields in the certificate. Extension fields, or simply extensions, define the usage of the certificate.
There are a few extensions defined in RFC 5280 that are commonly used and broadly supported, including 

* **Basic Constraints**
* **Key Usage**
* **Extended Key Usage**

In this exercise, you will create a codesigning certificate using the pre-built templates provided by ACM Private CA.

Follow these steps by right clicking and opening this link : [Template ACM Private CA](https://view.highspot.com/viewer/5dc858b666bbaa7b82d9c6d0)

Templates allow for constrained usage of certificates for specific usecases and IAM permissions can be used to control which principals - users
or roles that can issue a specific kind of certificate.

## Cleanup

#### AWS Event
Don't worry about cleanup, we will take care of it. Hopefully you've learned something useful in this workshop that you can take back your organization. Thank you for coming.

#### On Your Own
1. Disable and delete Root CA and Subordinate CA
2. Delete all three CloudFormation Templates

#### License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
