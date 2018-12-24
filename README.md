# AWS Data Protection Workshops

If you are dealing with data protection with methods such as encryption or certificate management within your AWS infrastructure, these workshops can help. We will be using the Cloud9 IDE and a combination of python code and AWS console access for these workshops.

# Ubiquitous Encryption 

Data encryption provides a strong layer of security to protect data that you store within AWS services. AWS provides tooling to achieve ubiquitous encryption 
for data in transit as well as data at rest.

<a><img src="images/ubiquitous-encryption.png" width="800" height="600"></a>

# Prerequisites

### AWS Account

In order to complete these workshops you'll need a valid, usable AWS Account with Admin permissions.  The code and instructions in these workshops assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you'll run into naming conflicts for certain resources. 

Use a **personal account** or create a new AWS account to ensure you have the neccessary access. This should not be an AWS account from the company you work for.

If the resources that you use for this workshop are left undeleted you will incur charges on your AWS account.

### Cloudformation templates for initial environment setup

Please run these cloudformation stacks in your AWS account as this is required for all the workshops

### Step 1 :

[![Deploy IAM user creation stack](images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=cryptobuilders-iam-user-creation&templateURL=https://s3.amazonaws.com/crypto-workshop-dont-delete/template-create-user.yaml)

The above stack creates an IAM user called **builder** .

### Before you proceed to Step 2

Please login into your account with the username **builder** . The password for this user is **reinvent**

### Step 2 :

[![Deploy workshops environment creation stack](images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=cryptobuilders-env-setup&templateURL=https://s3.amazonaws.com/crypto-workshop-dont-delete/template-env-setup.yaml)

The above stack creates an Cloud9 IDE environment called **workshop-environment** 

### Step 3 :

* Navigate to the Cloud9 service within your AWS console
* In the Cloud9 IDE environment you will find a folder called **data-protection-workshops** in the folder pane on the left side of the screen
* Open the file named **environment-setup.py**  in the IDE
* Run the python module **environment-setup.py** by clicking the play button <a><img src="images/cloud9-ide-play-button.png" width="50" height="30"></a>
 on the top pane 
* In the runner window below you should see **Workshop environment setup was successful** printed

# Workshops

**Please review and complete all the above prerequisites before attempting these workshops.**

<!DOCTYPE html>
<html>
<body>

<kbd>
<a href="https://github.com/aws-samples/crypto-builders/tree/master/identity-and-access-control"><img src="images/identity-access-control.png" width="352" height="240" title="click me"></a>
</kbd>
<kbd>
<a href="https://github.com/aws-samples/crypto-builders/tree/master/data-encryption"><img src="images/data-encryption.png" width="352" height="240" title="click me"></a>
</kbd>
<br>

</body>
</html>


### Browser

These workshops assume you are using a Cloud IDE environment. We recommend you use the latest version of Chrome or Firefox to complete this workshop.

## License Summary

This sample code is made available under a modified MIT license. See the [LICENSE](LICENSE) file.
