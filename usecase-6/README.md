## ACM Private Certificate Authority (ACM Private CA)

This workshop demonstrates how ACM Private Certificate authority(PCA) service can be used to create a complete CA hierarchy, generate a private certificate and apply the 
private certificate on an Application load balancer while following security best practices.

##### 1. You will be using a AWS provided account for this workshop.

* IF you are logged into your personal AWS account or your corporate AWS account, you should log out now.
* Open this link in a new browser tab: [AWS provided account](https://dashboard.eventengine.run/)
* Click on the **AWS Console** button
* It should bring up a pop-up screen. On the pop-up,  under Login Link click on **Open Console**
* You should be logged into the AWS provided account
* Please verify that the region selected is **N.Virginia**

### 2. An IAM Role called **CaAdminRole** is the role that a CA administrator would assume. 

* Assume the role named CaAdminRole by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Certificate Authority administrator will need for CA administration. As a CA administrator you will be responsible for creating a root and subordinate certificate authority
hierarchy

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)

### 3. Build the infrastructure needed for creating a CA hierarchy by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-ca-admin.yaml* [CA Admin Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-6/cf-templates/template-ca-admin.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. If you are not familiar with this, follow instructions here [Deploy Cloudformation Stack Instructions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-template.html)

### 4. Create a Root CA. 

* Navigate to ACM Service in the AWS Console
* Click Get Started under Private Certificate Authority
* Click this link for the rest of the steps : [Creating a Root CA](https://view.highspot.com/viewer/5d5b129b6a3b116f4230f242)

### 5. Create a Subordinate Issuing CA. 

* Navigate to ACM Service in the AWS Console
* Under Private CA's click on the **Create CA** button
* Click this link for the rest of the steps  : [Creating a Subordinate CA](https://view.highspot.com/viewer/5d5b12f7628ba2737b0f2c16)

### 6. Quiz time. Open this link in a new browser tab : [quiz](https://bit.ly/2yQ5IML)

### 7. An IAM Role called **AppDevRole** is the role that an application developer would assume. 

* Assume the role named **AppDevRole** by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Application developer will need for building an web aplication which is fronted by an application load balancer and behind the load balancer is a lambda origin that
provides the HTML code for a website. The application developer will also have permissions to issue a certificate under a certificate authority that they select.

### 8. Build the application infrastructure by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-appdev-admin.yaml* [AppDev Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-6/cf-templates/template-app-dev.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. IF you are not familiar with this, follow instructions here [Deploy Cloudformation Stack Instructions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-template.html)

### 9. Next step is to issue a private certificate to put on the application load balancer. 

Click on this link for steps : [Issue a private certificate](https://view.highspot.com/viewer/5d5b133d6a3b116f29313a10)  

### 10. Attach a HTTPS listener and private certificate to the ALB . 

Click on this link for steps : [Attach HTTPS Listener](https://view.highspot.com/viewer/5d5b5d496a3b116f1e31bd56)  

### 11. Validate the identity of the ALB from your browser. Please use the steps below for the browser that you are using

For firefox : [Validate Certificate Identity](https://view.highspot.com/viewer/5d5c1fe23f65f635ae005a47)  

For google chrome : [Validate Certificate Identity](https://view.highspot.com/viewer/5d5c42da66bbaa2fc928a575)

For Microsoft Edge : [Validate Certificate Identity](https://view.highspot.com/viewer/5d5c2e5cf7794d4833e8207a)

### 12. Quiz time. Open this link in a new browser tab : [quiz](https://bit.ly/2Zh3iRY)

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
