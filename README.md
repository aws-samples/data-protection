## ACM Private Certificate authority - Private certs for your webserver 

This workshop demonstrates ACM Private Certificate authority and how it can be used to generate private certs 

## Let's look at some concepts :

<a><img src="images/acm-pca-vs-public-ca.png" width="800" height="600"></a><br>

## Let's do some private cert generaton with AWS Certificate Manager(ACM) private certificate authority(PCA)

Open the Cloud9 IDE environment called **workshop-environment**. Within the Cloud9 IDE open the bash terminal and use the following command to checkout code for this usecase :

**git checkout acm-pca-usecase-5**

Once you run the command above you will see a folder called **usecase-5** in the Cloud9 environment. Follow the below steps:

### Step 1 

Run the python module named **intial_config.py**

This module will create a DynamoDB table called **shared_variables_crypto_builders** . The primary purpose of this table is to share variables
across the different python module that we will run in this usecase.

### Step 2 :

Run the python module named **usecase-5-part-1.py**

* This module creates a ACM private certificate authority called **reinvent.builder.subordinate**
* Run the **usecase-1.py** python module
* The module **usecase-1.py** uploads the ***plaintext_u.text*** file to an S3 bucket named reinvent-builderXXXX 
* Before the file is stored on S3 it is server side encrypted using the KMS key alias *kms_key_sse_usecase_1*

### Step 3 :

* In the AWS console,navigate to the S3 service
* Look for the bucket named reinvent-builderXXXX
* In the bucket there would be a file called    .This file was encrypted using a Data key under the KMS master key **key_sse_usecase_1**
* Take a look at the properties of the file ***encrypted_e.text***.You will find that it's encrypted using AWS-KMS as shown in the picture below

<a><img src="images/in-aws-console-sse.png" width="400" height="200"></a><br>

### Step 4 :

* The **usecase-1.py** python module does a S3 getobject API Call on ***encrypted_e.text***
* The ***encrypted_e.text*** file is decrypted on the S3 service and over TLS gets delivered to this environment
* In the folder **usecase-1** ,you should see a file called ***plaintext_cycled_u.txt*** 
* Check whether the contents of ***plaintext_u.txt*** and ***plaintext_u_cycled.txt*** is the same 

### Step 5 :

* Run **usecase-1-cleanup.py** python module 
* This modules deletes the kms key and it's alias that we created in **kms_key_creation.py**
* and also deletes all the files that were created in the **usecase-1** folder
* Please remember that every time you run **usecase-1-cleanup.py** ,if you want to re-run this uecase,
  you will have to start from **Step 1**