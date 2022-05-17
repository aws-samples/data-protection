# ACM Private Certificate Authority (ACM Private CA)

## Internal HTTPS Application use case

#### 7. An IAM Role called **AppDevRole** is the role that an application developer would assume. 

* Assume the role named **AppDevRole** by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that a Application developer will need for building an web aplication which is fronted by an application load balancer and behind the load balancer is a lambda origin that
provides the HTML code for a website. The application developer will also have permissions to issue a certificate under a certificate authority that they select.

* If you are not familiar with switching roles, follow this tutorial if needed: [Assume Role in Console](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/SwitchRole.pdf)

#### 8. Build the application infrastructure by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-appdev.yaml* [AppDev Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-9/cf-templates/template-app-dev.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. If you are not familiar with this, follow instructions here by right clicking and opening link in a new browser tab [Deploy AppDev Cloudformation Stack Instructions](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/AppDevSteps.pdf)
This cloudformation deployment takes about 3 minutes to complete.

#### 9. Next step is to issue a private certificate to put on the application load balancer. 

* Open this link in a new browser tab for steps : [Issue a private certificate](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/IssuePrivateCertificate.pdf)  
* [Quiz](https://bit.ly/2KXE06k)

#### 10. Attach a HTTPS listener and private certificate to the ALB. 

* Open this link in a new browser tab for steps : [Attach HTTPS Listener](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/ApplyCertToLoadBalancer.pdf)  
* [Quiz](https://bit.ly/2Hh1lin)

#### 11. Validate the identity of the ALB with the browser that your are using. Please open link in a new browser tab

For Firefox: [Validate Certificate Identity on Firefox Browser](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/ValidateALBIdentityFirefox.pdf)  

For Google Chrome: [Validate Certificate Identity on Chrome Browser](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/ValidateALBIdentityChrome.pdf)

For Microsoft Edge: [Validate Certificate Identity on Microsoft Edge Browser](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/ValidateALBIdentityEdge.pdf)

For Google Chrome on Windows: [Validate Certificate Identity on Windows](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/WindowsALBCert.pdf)

#### 12. Quiz time. Open this link in a new browser tab: [quiz](https://bit.ly/2Zh3iRY)

