# AWS Data Protection Workshops

If you are considering protecting data in your [AWS](https://aws.amazon.com/) environment using methods such as encryption or certificate management, these workshops can help you learn in depth. We will be using the [Cloud9 IDE environment](https://aws.amazon.com/cloud9/) and a combination of [Python](https://www.python.org/) code and AWS console access for these workshops.

# Ubiquitous Encryption 

Data encryption provides a strong layer of security to protect data that you store within AWS services. AWS services can help you achieve ubiquitous encryption 
for data in transit as well as data at rest.

<a><img src="./images/ubiquitous-encryption.png" width="989" height="557"></a>

# Prerequisites

### AWS Account

If you are participating in this workshop as part of an AWS event, pre-provisioned temporary accounts that are specifically initialized for this workshop might be provided by the organizers. To access your temporary account you will receive a **12-digit hash code** that can be used at the [AWS Event Engine Site](https://dashboard.eventengine.run). You will not need a username and password.

If you wish to participate in this workshop without a pre-provisioned temporary account, please see the [AWS Initialization and tear down](#aws-initialization-tear-down) section below.

### Browser

These workshops assume that you are using the [Cloud9 IDE environment](https://aws.amazon.com/cloud9/). We recommend you use the latest version of Chrome or Firefox to complete this workshop. 

### Knowledge Of Python Programming Language

Basic python knowledge is sufficient to consume these workshops.

# Setup Workshop Environment

* Navigate to the Cloud9 service within your AWS console
* Open the Cloud9 IDE environment called **workshop-environment**. It takes about 30 seconds for the environment to start up.
* In the Cloud9 IDE environment you will find a folder called **data-protection** in the folder pane on the left side of the screen
* Right-click (on MacOS: control-click) the file named **environment-setup.sh**  in the IDE and select **Run**
* This script takes about a minute to complete
* In the runner window below you should see **SUCCESS: installed python dependencies ** followed by a list of the installed packages

# Workshops

These workshops demonstrates server side encryption, client side encryption and certfificate management concepts within AWS. For example :

* How do I put an object on S3 with server side encryption ?
* How do I use aws encryption sdk to encrypt data in my application before sending the data to an AWS service ?
* What is Data Key Caching ?
* How can I generate X.509 certificates with AWS Certificate Manager to enable TLS on my load balancer ?
* How do I use AWS Certificate Manager to generate a private certificate authority ?

| Title | Description | Learning Time | Teaching Time With Discussion | 
| :------- | :---------- | :-- | :-- |
| [Level 200: Server Side Encryption](./usecase-1/)  | This workshop demonstrates server side encryption on S3 | 15 min | 30 min |
| [Level 200: Client Side Encryption](./usecase-2/)  | This workshop demonstrates client side encryption | 15 min | 30 min |
| [Level 200: Client Side Encryption With Data Key Caching](./usecase-3/)  | This workshop demonstrates client side encryption with data key caching | 15 min | 30 min |
| [Level 300: Creating Private Certs ACM Private Certificate Authority - Mode-1 ](./usecase-4/)  | This workshop demonstrates how you create a AWS Certificate Manager private certificate authority(PCA) and use ACM PCA to sign a CSR to create a private certificate | 40 mins | 1 hour |
| [Level 300: Creating Private Certs ACM Private Certificate Authority - Mode-2 ](./usecase-5/)  | This workshop demonstrates how you create a AWS Certificate Manager private certificate authority and use this CA to create private X.509 certififcates for a private domain | 40 mins | 1 hour |

**NOTE:** The ACM PCA use cases (the latter 2) can only be run within the VPC where the ALB is deployed as a private DNS name space is used. This will work within the Cloud9 IDE but not from machines that are outside of the VPC. 

<hr/>

# AWS Initialization & tear down

**IMPORTANT!** 
* This section is only relevant if you are **not** using a pre-provisioned account. 
* The resources used in this workshop **will incur charges** in the AWS account used if not torn down according to the procedure outlined below

You can use a **personal account** or create a **new AWS account** to ensure you have the neccessary access. This should not be an AWS account from the company you work for. Please note that creating an AWS account takes time (credit card validation, etc.) and is not recommended when participating in the workshop during a time constrained event.

### Region Support

Since these workshops use the Cloud9 IDE, you can use run these workshops in the following regions where the AWS Cloud9 
service is available : 
* **N.Virginia** (us-east-1)
* **Ohio** (us-east-2)
* **Oregon** (us-west-2)
* **Ireland** (eu-west-1)
* **Singapore** (ap-southeast-1)

### Cloudformation templates for initial environment setup

Please download the [Data Protection Workshop cloudformation stack](./cf-templates/template-workshops-setup.yaml) and launch it in your AWS account as this is required for all the workshops in this repository. To launch the stack you must go to the AWS Console and navigate to the CloudFormation service where you can choose **Create Stack** and upload the Cloudformation stack for the workshop. You provide a name for the stack and keep clicking **next** until you get to the point where it says:

```
I acknowledge that AWS CloudFormation might create IAM resources with custom names.
```

Acknowledge the above statement by clicking on the check box and then click on the **Create** button

The above stack creates an Cloud9 IDE environment called **workshop-environment**. 
In addition a VPC with two subnets and an internet gateway is also created.


### Tear down Cloudformation stack

After you have completed the workshop, you need to tear down the stack by navigating to the CloudFormation service in the AWS console and selecting the stack name you chose when launching the stack. 

Choose the **delete** action and wait for the process to complete. Note that it can take a few minutes for the stack to clean up its resources.

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.


