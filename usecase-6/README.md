## ACM Private Certificate authority - Generating and using private certificates for a private domain

This workshop demonstrates how ACM Private Certificate authority(PCA) service can be used to create a complete CA hierarchy, generate a private certificate and apply the 
private certificate on an Application load balancer while following security best practices.

### 1. An IAM Role called CaAdminRole is the role that a CA administrator would assume. 

* Assume the role named CaAdminRole by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Certificate Authority administrator will need for CA administration. As a CA administrator you will be responsible for creating a root and subordinate certificate authority
hierarchy

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)

### 2. Build the infrastructure needed for creating a CA hierarchy by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-ca-admin.yaml* [CA Admin Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-6/cf-templates/template-ca-admin.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. If you are not familiar with this, follow instructions here [Deploy Cloudformation Stack Instructions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-template.html)


### 3. Create a Root CA. 
* Navigate to ACM PCA Service

* Click Private CAs tab

* Click Create CA

* Click this link for the rest of the steps : [Creating a Root CA](https://view.highspot.com/viewer/5d5b129b6a3b116f4230f242)

### 4. Create a Subordinate Issuing CA. 

* Navigate to ACM PCA Service

* Click Private CAs tab

* Click Create CA

* Click this link for the rest of the steps  : [Creating a Subordinate CA](https://view.highspot.com/viewer/5d5b12f7628ba2737b0f2c16)

### 5. Quiz time. Open the link below in a new browser tab

[quiz](https://bit.ly/2yQ5IML)

### 6. An IAM Role called **AppDevRole** is the role that an application developer would assume. 

* Assume the role named **AppDevRole** by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Application developer will need for building an web aplication which is fronted by an application load balancer and behind the load balancer is a lambda origin that
provides the HTML code for a website. The application developer will also have permissions to issue a certificate under a certificate authority that they select.

### 7. Build the application infrastructure by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-appdev-admin.yaml* [AppDev Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-6/cf-templates/template-app-dev.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. IF you are not familiar with this, follow instructions here [Deploy Cloudformation Stack Instructions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-template.html)

### 8. Next step is to issue a private certificate to put on the application load balancer. 

Click on this link for steps : [Issue a private certificate](https://view.highspot.com/viewer/5d5b133d6a3b116f29313a10)  

### 9. Attach a HTTPS listener and private certificate to the ALB . 

Click on this link for steps : [Attach HTTPS Listener](https://view.highspot.com/viewer/5d5b5d496a3b116f1e31bd56)  

### 10. Validate the identity of the ALB from your browser. Please use the steps below only for the browser that you are using

For firefox :

[Validate Certificate Identity](https://view.highspot.com/viewer/5d5c1fe23f65f635ae005a47)  

For google chrome :

[Validate Certificate Identity](https://view.highspot.com/viewer/5d5c42da66bbaa2fc928a575)

For Microsoft Edge :

[Validate Certificate Identity](https://view.highspot.com/viewer/5d5c2e5cf7794d4833e8207a)

### 11. Quiz time. Open a link below in a new browser tab

The **“AppDevRole”** has certain IAM permissions associated with the role. Take this quiz by following this link : [quiz](https://bit.ly/2Zh3iRY)

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
