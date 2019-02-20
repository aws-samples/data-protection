# AWS Data Protection Workshops

If you are dealing with protecting data on your AWS architecture using methods such as encryption or certificate management, these workshops can help you learn in depth. We will be using the Cloud9 IDE and a combination of python code and AWS console access for these workshops.

# Ubiquitous Encryption 

Data encryption provides a strong layer of security to protect data that you store within AWS services. AWS services can help you achieve ubiquitous encryption 
for data in transit as well as data at rest.

<a><img src="images/ubiquitous-encryption.png" width="700" height="500"></a>

# Prerequisites

### AWS Account

In order to complete these workshops you'll need a valid active AWS Account with Admin permissions.  The code and instructions in these workshops assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you'll run into naming conflicts for certain resources. 

Use a **personal account** or create a new AWS account to ensure you have the neccessary access. This should not be an AWS account from the company you work for.

If the resources that you use for this workshop are left undeleted you will incur charges on your AWS account.

### Browser

These workshops assume that you are using a Cloud IDE environment. We recommend you use the latest version of Chrome or Firefox to complete this workshop.

### Knowledge Of Python Programming Language

Basic python knowledge is sufficient to consume these workshops.

### Region Support

Since these workshops use the Cloud9 IDE, you can use run these workshops in the following regions where the  AWS Cloud9 
service is available : **N.Virginia, Ohio, Oregon, Ireland and Singapore.**

### Cloudformation templates for initial environment setup

Please run these cloudformation stacks in your AWS account as this is required for all the workshops in this repository. When you launch
the Cloudformation stack keep clicking next until you get to the point where it says 

**"I acknowledge that AWS CloudFormation might create IAM resources with custom names."**

Acknowledge the above statement by clicking on the check box and then click on the **Create** button

### Step 1 : (Launch CF Stack)

[![Deploy workshops environment creation stack](images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=data-protection-env-setup&templateURL=https://s3.amazonaws.com/crypto-workshop-dont-delete/template-env-setup.yaml)

The above stack creates an Cloud9 IDE environment called **workshop-environment** . In addition a VPC with two subnets and
an internet gateway is also created.

### Step 2 : (Cloud9 IDE Environment Setup)

* Navigate to the Cloud9 service within your AWS console
* Open the Cloud9 IDE environment called **workshop-environment** .It takes about 30 seconds for the
  environment to start up.
* In the Cloud9 IDE environment you will find a folder called **data-protection** in the folder pane on the left side of the screen
* Open the file named **environment-setup.py**  in the IDE
* Run the python module **environment-setup.py** by clicking the play button <a><img src="images/cloud9-ide-play-button.png" width="50" height="30"></a>
  on the top pane 
* This module would take about a minute to complete
* In the runner window below you should see **Workshop environment setup was successful** printed

### Step 3 : (Initiating CF stacks creation)

* Within the Cloud9 environment, open the file named **cf-setup.py** in the IDE
* Run the python module **cf-setup.py** by clicking the play button <a><img src="images/cloud9-ide-play-button.png" width="50" height="30"></a>
  on the top pane 
* In the runner window below you should see **All cloudformation stack creation for the workshops has been initiated** printed
* It takes about 5 minutes for all cloudformation stacks creation to complete. Once complete you should see the
  following stacks successfully completed as shown in the picture below :

<a><img src="images/cf-template-complete-pic.png" width="700" height="300"></a>

### Step 3 : (Change directory)

* Open a bash terminal within the Cloud9 environment and change directory to **data-protection **. See Images below
* At this point the cloud9 environment is ready for the workshops

<a><img src="images/bash-terminal-environment.png" width="700" height="300"></a>

# Workshops

**Please review and complete all the above prerequisites before attempting these workshops. The images below are clickable links**

<!DOCTYPE html>
<html>
<body>

<kbd>
<a href="https://github.com/aws-samples/data-protection/tree/identity-and-access-control"><img src="images/identity-access-control.png" width="352" height="240" title="click me"></a>
</kbd>
<kbd>
<a href="https://github.com/aws-samples/data-protection/tree/data-encryption"><img src="images/data-encryption.png" width="352" height="240" title="click me"></a>
</kbd>
<br>

</body>
</html>

# Final Cleanup

Once you you have finished working on the workshops within this repository ,the final step is to clean up the resources by deleting
the cloudformation stacks that setup the workshop environment. For cleanup follow the steps below :

### Step 1 :

Within the Cloud9 IDE **workshop environment** that you used for this workshop checkout the final clean up branch
by using the following command :

**git checkout final-cleanup**

### Step 2 :

* In the Cloud9 IDE you will find a python module called ***final-cleanup.py***
* Run the **final-cleanup.py** python module 
* At this point cleanup of the cloudformation stacks is intitiated
* It takes about 3 minutes for the cloudformation stacks named **data-protection-env-setup** to be deleted
* The Cloud9 IDE **workshop environment** session shall will be terminated at this point

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.


