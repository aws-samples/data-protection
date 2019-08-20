## ACM Private Certificate authority - Generating and using private certificates for a private domain

This workshop demonstrates how ACM Private Certificate authority(PCA) service can be used to create a complete CA hierarchy, generate a private certificate and apply the 
private certificate on an Application load balancer.

### 0. Deploy initial CloudFormation Template
[Base CloudFormation Stack](cf-templates/template-acm-pca.yaml)

### 1. An IAM Role called CaAdminRole is the role that a CA administrator would assume. 

* Assume the role named CaAdminRole by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Certificate Authority administrator will need for CA administration. As a CA administrator you will be responsible for creating a root and subordinate certificate authority
hierarchy

### 2. Build the infrastructure needed for creating a CA hierarchy by deploying the cloudformation template below

Please download the [CA Admin cloudformation stack](cf-templates/template-ca-admin.yaml) and launch it in your AWS account. To launch the stack you must go to the AWS Console and navigate to the CloudFormation service where you can choose **Create Stack** and upload the Cloudformation stack for the workshop. You provide a name for the stack and keep clicking **next** until you get to the point where it says:

```
I acknowledge that AWS CloudFormation might create IAM resources with custom names.
```

### 3. Create a Root CA. 
* Navigate to ACM PCA Service

* Click Private CAs tab

* Click Create CA

* Click link below for rest of steps : [Creating a Root CA](https://view.highspot.com/viewer/5d5b129b6a3b116f4230f242)

### 4. Create a Subordinate Issuing CA. 

* Navigate to ACM PCA Service

* Click Private CAs tab

* Click Create CA

* Click link below for rest of steps : [Creating a Subordinate CA](https://view.highspot.com/viewer/5d5b12f7628ba2737b0f2c16)

### 5. Quiz time. Open a link below in a new browser tab

[quiz](https://bit.ly/2yQ5IML)

### 6. An IAM Role called AppDevRole is the role that an application developer would assume. 

* Assume the role named AppDevRole by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Application developer will need for building an web aplication which is fronted by an application load balancer and behind the load balancer is a lambda origin that
provides the HTML code for a website. The application developer will also have permissions to issue a certificate under a certificate authority that they select.

### 7. Build the infrastructure by deploying the cloudformation template below

Please download the [Application Developer cloudformation stack](cf-templates/template-app-dev.yaml) and launch it in your AWS account. To launch the stack you must go to the AWS Console and navigate to the CloudFormation service where you can choose **Create Stack** and upload the Cloudformation stack for the workshop. You provide a name for the stack and keep clicking **next** until you get to the point where it says:

```
I acknowledge that AWS CloudFormation might create IAM resources with custom names.
```

### 8. Next step is to issue a private certificate to put on the application load balancer. 

Click the link below for steps

[Issue a private certificate](https://view.highspot.com/viewer/5d5b133d6a3b116f29313a10)  

### 9. Attach a HTTPS listener and private certificate to the ALB . 

Click link below for steps

[Attach HTTPS Listener](https://view.highspot.com/viewer/5d5b5d496a3b116f1e31bd56)  

### 10. Validate the identity of the ALB by your browser 

For firefox :

[Validate Certificate Identity](https://view.highspot.com/viewer/5d473e2978e87d12c129ca1b)  

For google chrome :

TBD

For Microsoft Edge :

TBD

### 11. Cleanup - Perform this step only if you are doing this exercise on your own. If you are doing this workshop as part of a AWS managed marketing event where a AWS account is provided for you, there is no need to cleanup 

* Delete the HTTPS listener to the ALB
* Delete the private certificate that you created
* Disable and Delete the root and subordinate CA's that you created 
* Assume the IAM role named CaAdmin and delete the cloudformation template that you created
* Assume the IAM role named AppDevRole and delete the cloudformation template that you created

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
