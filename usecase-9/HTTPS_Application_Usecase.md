# ACM Private Certificate Authority (ACM Private CA)

## Internal HTTPS Application use case

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

Open this link in a new browser tab for steps : [Attach HTTPS Listener](https://view.highspot.com/viewer/604a5e03f7794d6f72494487)  

#### 11. Validate the identity of the ALB with the browser that your are using. Please open link in a new browser tab

For Firefox: [Validate Certificate Identity on Firefox Browser](https://view.highspot.com/viewer/5d5c1fe23f65f635ae005a47)  

For Google Chrome: [Validate Certificate Identity on Chrome Browser](https://view.highspot.com/viewer/5d5c42da66bbaa2fc928a575)

For Microsoft Edge: [Validate Certificate Identity on Microsoft Edge Browser](https://view.highspot.com/viewer/5d5c2e5cf7794d4833e8207a)

For Google Chrome on Windows: [Validate Certificate Identity on Windows](https://view.highspot.com/viewer/5dcadc15b7b739360b417fb5)

#### 12. Quiz time. Open this link in a new browser tab: [quiz](https://bit.ly/2Zh3iRY)

