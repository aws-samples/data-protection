## Server Side Encryption 

This workshop demonstrates server side encryption using AWS KMS and S3

## Let's look at some concepts :

<a><img src="images/data-at-rest-encryption-primer.png" width="700" height="500"></a><br>
<a><img src="images/server-side-encryption-in-aws.png" width="700" height="500"></a><br>

## Let's do some server side encryption

Open the Cloud9 IDE environment called **workshop-environment** and navigate to the **data-protection/usecase-1** directory.
Follow the recipe below:

### 1. Run the module named `kms_key_creation-Step-1.py`

This module will create a KMS master key with the key alias **kms_key_sse_usecase_1** . In the following steps we will refer to this
master key using the alias. Browse to the KMS console and you should find the key alias **kms_key_sse_usecase_1** under 
customer managed keys

### 2. Run the module named `usecase-1-Step-2.py`

This module uploads the ***plaintext_u.txt*** file to an S3 bucket named `dp-workshop-builderXXXX`. 
Before the file is stored on S3 it is server side encrypted using the KMS key alias *kms_key_sse_usecase_1*

### 3. Inspect the encrypted file in S3

In the AWS console, navigate to the S3 service and look for the bucket named `dp-workshop-builderXXXX`.
In the bucket there should be a file called ***encrypted_e.txt***. This file was encrypted using a Data key under the KMS master key **key_sse_usecase_1**. Take a look at the properties of the file ***encrypted_e.txt***. You will find that it's encrypted using AWS-KMS as shown in the picture below:

<a><img src="images/in-aws-console-sse.png" width="400" height="200"></a><br>

### 4. Compare the decrypted file from S3 with the original

The `usecase-1-Step-2.py` python module does a S3 getobject API Call on ***encrypted_e.txt*** which is decrypted by the S3 service and retrieved over TLS into your Cloud9 environment. In the folder **usecase-1** ,you should see a file called ***plaintext_cycled_u.txt***. Compare its contents to the original file named ***plaintext_u.txt***. 

### 5. Run the module named `usecase-1-cleanup-Step-3.py`

This modules deletes the kms key and it's alias that we created in **kms_key_creation-Step-1.py** and also deletes all the files that were created in the **usecase-1** folder. Please remember that when you run `usecase-1-cleanup-Step-3.py` and you want to re-run this use case, you will have to start from the beginning.