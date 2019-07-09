## Client Side Encryption

This workshop demonstrates client side encryption 

## Let's do some client side encryption

Open the Cloud9 IDE environment called **workshop-environment** and navigate to the **data-protection/usecase-2** directory.
Follow the steps below:

### 1. Run the module named `kms_key_creation-Step-1.py`

* You should see **"KMS Master Key with alias name kms_key_cse_usecase_3 successfully created"** printed
  in the runner window pane below.
* This python module will create a KMS master key with the key alias **kms_key_cse_usecase_2** 
* Browse to the KMS console and you should find the key alias **kms_key_cse_usecase_2** under 
  customer managed keys

### 2. Run the **usecase-2-Step-2.py** python module . 

* The runner pane should print **"Module run was successful !!"**
* You will find a file called ***plaintext_u.txt*** which is the plaintext unencrypted file
* The module **usecase-2-Step-2.py** encrypts the ***plaintext_u.txt*** file
* The encrypted file is created and is called ***encrypted_e.txt***
* You should see **"Module run was successful"** printed in the runner window pane below

### 3. Check the decrypted file

* The encrypted file ***encrypted_e.txt*** is then decrypted 
* The decrypted file is called ***plaintext_u_cycled.txt***

### 4. Check whether the encryption and decryption process was successful

* Check whether the***plaintext_u.txt*** and ***plaintext_u_cycled.txt*** have the same content
* This indicates that the client side encryption and then decryption was successful

### 5. Wait for 2 minutes and then Run the **check-gendatakey-Step-3.py** python module

* The **check-gendatakey-Step-3.py** is checking for whether a GenerateDataKey API call was logged by cloudtrail
  and this event was then sent to a cloudwatch event rule.
* If all things go well, you should see **"GenerateDataKey API Called"** in the runner window below. If you don'things
  see this print wait for a minute and try again

### 6. Run the **usecase-2-cleanup-Step-4.py** python module 

* You should see **Cleanup Successful** printed in the runner window pane below
* This modules deletes the kms key and it's alias that we created in **kms_key_creation-Step-1.py**
  .It also deletes all the files that were created in the **usecase-2** folder
* Please remember that every time you run **usecase-2-cleanup-Step-4.py** ,if you want to re-run this uecase,
  you will have to start from **Step 1**

### Some questions to think about :

* Why do we wait for 2 minutes in Step 5 ?
