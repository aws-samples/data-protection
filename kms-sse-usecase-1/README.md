## Server Side Encryption 

This workshop demonstrates server side encryption using AWS KMS and S3

## Let's look at some concepts :

<a><img src="images/data-at-rest-encryption-primer.png" width="800" height="600"></a><br>
<a><img src="images/server-side-encryption-in-aws.png" width="800" height="600"></a><br>
<a><img src="images/aws-kms-key-hierarchy.png" width="800" height="600"></a><br>

## Let's do some server side encryption

Open the Cloud9 IDE environment called **workshop-environment**. Within the Cloud9 IDE open the bash terminal and use the following command to checkout code for this usecase :

**git checkout kms-sse-usecase-1**

Once you run the command above you will see a folder called **usecase-1** in the Cloud9 environment. Follow the below steps:

### Step 1 :

Run the module named **kms_key_creation.py**

This module will create a KMS master key with the key alias **kms_key_sse_usecase_1** . In the following steps we will refer to this
master key using the alias.

### Step 2 :

* You will find a file called ***plaintext_u.txt*** which is the plaintext unencrypted file
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