## ACM Private Certificate authority - Generating and using private certificate for a private domain

This workshop demonstrates how ACM Private Certificate authority(PCA) service can be used to create a complete CA hierarchy, generate a private certificate and apply the 
private certificate on an Application load balancer.

### Cloudformation templates for initial environment setup

Please download the [Certificate management Workshop cloudformation stack](cf-templates/template-acm-pca.yaml) and launch it in your AWS account. To launch the stack you must go to the AWS Console and navigate to the CloudFormation service where you can choose **Create Stack** and upload the Cloudformation stack for the workshop. You provide a name for the stack and keep clicking **next** until you get to the point where it says:

```
I acknowledge that AWS CloudFormation might create IAM resources with custom names.
```

Acknowledge the above statement by clicking on the check box and then click on the **Create** button

The above stack creates an Cloud9 IDE environment called **workshop-environment**. 
In addition a VPC with two subnets and an internet gateway is also created.

## Cloud9 environment setup 

Open the Cloud9 IDE environment called `workshop-environment` in your AWS account and follow the steps below:

### 1. Run the module named `environment-setup.sh`

This shell script sets up the Cloud9 environment 

### 2. Run the module named `usecase-6-setup.py`

This module takes about 30 seconds to complete and will create the CRL Bucket for the ACM private CA and register the lambda function as the ALB target

### 3. An IAM Role called CaAdminRole is the role that a CA administrator would assume. Assume the role named CaAdminRole by using switch role on the AWS console in the AWS account that you are currently logged into

This role has permissions that a Certificate Authority administrator will need for CA administration. As a CA administrator you will be responsible for creating a root and subordinate certificate authority
hierarchy

### 4. Create a Root CA. Click link below for steps

[Creating a Root CA](https://view.highspot.com/viewer/5d544bdd030dc833da6f2daf)

### 5. Create a subordinate issuing CA. Click link below for steps
 
[Creating a Subordinate CA](https://view.highspot.com/viewer/5d473d0e628ba23f42792a44)

### 5. quiz time. Open a link below in a new browser tab

[quiz](https://bit.ly/2yQ5IML)

### 3. An IAM Role called AppDevRole is the role that an application developer would assume. Assume the role named AppDevRole by using switch role on the AWS console in the AWS account that you are currently logged into

This role has permissions that a Application developer will need for building an web aplication which is fronted by an application load balancer and behind the load balancer is a lambda origin that
provides the HTML code for the website. The application developer will also have permissions to issue a certificate under a certificate authority that they select.

### 6. Build the infrastructure by running a cloudformation template 

Please download the [Application Developer cloudformation stack](cf-templates/template-app-dev.yaml) and launch it in your AWS account. To launch the stack you must go to the AWS Console and navigate to the CloudFormation service where you can choose **Create Stack** and upload the Cloudformation stack for the workshop. You provide a name for the stack and keep clicking **next** until you get to the point where it says:

```
I acknowledge that AWS CloudFormation might create IAM resources with custom names.
```

### 6. Next step is to issue a private certificate to put on the application load balancer. Click the link below for steps

[Issue a private certificate](https://view.highspot.com/viewer/5d473d39030dc823ac380521)  

### 7. Attach a HTTPS listener and private certificate to the ALB . Click link below for steps

[Attach HTTPS Listener](https://view.highspot.com/viewer/5d473d7a659e935fa5fcd237)  

### 8. Validate the identity of the ALB by your browser 

For firefox :

[Validate Certificate Identity](https://view.highspot.com/viewer/5d473e2978e87d12c129ca1b)  

For google chrome :

TBD

For Microsoft Edge :

TBD

### 9. Within the Cloud9 environment run the module named `usecase-6-cleanup.py`

This is the step for cleaning up some of the resources that were created for this use case.

This module cleans up all the local files, S3 buckets, target groups,listeners that was created in the python modules for this usecase.
Please make sure that you run this cleanup script. Otherwise you will continue accruing charges for the ACM private certificate authority that was created during this usecase
You should see the following printed in the runner window pane:
```
Everything cleaned up, you are all good !!
```

### Tear down Cloudformation stack

After you have completed the workshop, you need to tear down the stack by navigating to the CloudFormation service in the AWS console and selecting the stack name you chose when launching the stack. 

Choose the **delete** action and wait for the process to complete. Note that it can take a few minutes for the stack to clean up its resources.

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
