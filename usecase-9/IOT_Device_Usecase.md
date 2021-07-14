## IOT device certificates :

If you are building IOT applications where client devices need to validate their identity to central control servers, you could use AWS IOT core or your own control server that your organization has built. In this section of the workshop, we will go through a hands on exercise showing you how you get client device certificates and deploy them to an IOT device simulator and also how the AWS IOT core validates these device certificates to establish a successful TLS connection.

### 0. Create the base template

Run the CF template stack template-security-admin.yaml in your AWS account.

### 1. An IAM Role called **IOTDevRole** is the role that an IOT developer would assume. 

* Assume the role named **IOTDevRole** by using switch role on the AWS console in the AWS account that you are currently logged into

* This role has permissions that an IOT developer will need for building the necessary resources for IOT device certificate authentication use case.

* If you are not familiar with switching roles, follow this tutorial if needed: Right click on [Assume Role in Console](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/SwitchRole.pdf)

#### 2. Build the infrastructure needed for the IOT usecase by deploying the cloudformation template below

Please download the CF template by right clicking and save link as the filename *template-iot-dev.yaml* [IOT Developer Cloudformation Stack](https://raw.githubusercontent.com/aws-samples/data-protection/master/usecase-9/cf-templates/template-iot-dev.yaml) by right clicking and saving the yaml file on your laptop. 

Upload and launch the cloudformation stack in your AWS account. If you are not familiar with this, follow instructions here by right clicking and opening link in a new browser tab [Deploy IOT Developer Cloudformation Stack Instructions](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/IoTStackSteps.pdf)
This cloudformation deployment takes about 2 minutes to complete.

#### 3. For the next section, you need a Cloud9 IDE environment setup for executing code. PLease follow the instructions below :

* Navigate to the Cloud9 service within your AWS console
* Open the Cloud9 IDE environment called **IOT usecase environment**. It takes about 30 seconds for the environment to start up.
* In the Cloud9 IDE environment you will find a folder called **usecase-9** in the folder pane on the left side of the screen
* Delete that folder

Within your Cloud9 environment open the **usecase-9** directory

* Right-click (on MacOS: control-click) the file named **environment-setup.sh** in the IDE and select Run
* This script takes about a minute to complete
* The script installs various tools and packages for this section of the workshop, see the comments in the script for more information
* The script is finished when you see **environment setup complete**, additional log info can be found in the file `setup.log`

#### 4. Create the verification certificate and get it signed by the Subordinate CA that you had created earlier

The verification certificate is needed because that's the mechanism that the AWS IOT core uses to ascertain that you have access to the  Subordinate CA for signing an end entity certificate. There is also a registration code that's needed in the process and this code is used by the AWS IOT core to ascertain that the principal creating and uploading the verification certificate operation has permissions to access to the IOT Core within the AWS console.

In the Cloud9 environment :

Open a bash terminal. 

Change directory to /home/ec2-user/environment by using the following command :

```
cd /home/ec2-user/environment/data-protection/usecase-9
```


Generate a RSA 2048 key pair using the command below. A file verification_cert.key will be created.

```
openssl genrsa -out verification_cert.key 2048
```

Each AWS account has a unique IOT registration code. As part of the verification process, the common name of the CSR(Certificate signing request) must be set to the registration code.

Let's get the registration code from IOT core to put into the Common name for the CSR. Copy the registration code to your clipboard.

```
aws iot get-registration-code
```

We will now generate the verification certificate signing request(CSR). Fill in values at the prompt and when prompted for `Common name` enter the registration code(without quotes) as returned by the above command. For other parameters choose anything you like. Don't put anything for the challenge password or optional company name, just press enter two times and it should be good.

```
openssl req -new -key verification_cert.key -out verification_cert.csr
```

You should see the file verification_cert.csr generated.

The verification_cert.csr will be now signed by the subordinate CA that you created earlier and the certificate content is put into a .pem file

Run the script `verification-cert.sh` using the command below :

```
bash verification-cert.sh
```

This script will issue the verification certificate and also get the subordinate CA certificate from ACM PCA and upload it to the S3 bucket named `certificate-holder-<your-account-number>`. The bucket would be in the region that you are currently operating in.

At this point the AWS IOT core service has determined that you have the necessary permissions to sign a device certificate using the subordinate CA in your account.

#### 5. Download the subordinate CA certificate and verification certificate from the S3 bucket into your laptop

Follow the instructions here :

Right click and open [Download Verification cert and subordinate CA cert](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/DownloadCAVerificationCert.pdf)


#### 6. Register the CA by uploading Subordinate CA certificate and Verification certificate to IOT core on the AWS console

Follow the instructions here :

Right click and open [Register a CA ](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/UploadVeriCertSubordinateCAIOTCore.pdf)

Now the IOT core is loaded with the subordinate CA certificate. This means that any device certificate that's signed by the Subordinate CA can be trusted and validated by the IOT core.

#### 7. Let's create a device certificate in the Cloud9 environment

In this step you will create a device certificate that you will then associate with an IOT thing. Within the Cloud9 environment, open a terminal and execute the following commands to create a RSA key pair for the IOT device:

```
openssl genrsa -out device_cert.key 2048
```

Let's generate the CSR for the IOT device. For the CSR Parameters, you can put "iotdevice1" for Common name but for all other parameters its your choice. Don't set anything for the challenge password and the optional company name. Just press enter for those parameters. Use the following command to generate the CSR(Certificate signing request)

```
openssl req -new -key device_cert.key -out device_cert.csr
```

Run the script `device-cert.sh` which will issue the device certificate and get it signed by the subordinate CA that you created earlier and upload it to the S3 bucket named `certificate-holder-<your-account-number>`. You can use the command below :

```
bash device-cert.sh
```

#### 8. Download the device certificate from S3 back to the Cloud9 environment

Go to the S3 console and follow the instructions below :

Right click and open [Download the device cert from S3](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/DownloadDeviceCert.pdf)

#### 9. Create the IOT Policy that provides permissions for publishing and subscribing to a IOT topic

The IOT policy attached to a thing or a device provides permissions to a device or a thing for topics the IOT thing can publish and subscribe to. The policy also provides the ability to add a name to the thing that connects to the IOT core.

Follow the instructions here :

Right click and open [Create IOT policy](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/CreateIOTPolicy.pdf)

You have now created a policy called `alexa_temperature_policy` . This policy will allow a IOT device to publish to a topic named 'alexa/temperature'. For example think of a IOT device recording temperature and is publishing to this IOT topic called `alexa/temperature`. You will attach the policy to a IOT thing in later steps.

#### 10. Register the device certificate and create a thing within the IOT core service

Follow the instructions here :

Right click and open [Create and register a IOT thing](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/RegisterAThing.pdf)

#### 11. Configuring the MQTT(Standard for IOT Messaing) Client 

We will be using a MQTT client to simulate a IOT device. An MQTT cliens has been pre-installed in your Cloud9 environment. The mqtt client needs to communicate with the IOT core endpoint and the various certificates and keys required for a mutual TLS connection between the mqtt client and the AWS IOT core endpoint have been configured within the config.properties mqq configuration file.

Open the mqtt configuration file from a bash terminal in your Cloud9 environment:
```
c9 open /home/ec2-user/.mqtt-cli/config.properties 
```

In a bash terminal withiny our Cloud9 environment, use the following cli command in the terminal to get the mqtt endpoint URL or mqtt host
```
aws iot describe-endpoint --endpoint-type iot:Data-ATS
```
The output will be in this format 

{
    "endpointAddress": "b12qfcnz2tnjiu-ats.iot.us-east-1.amazonaws.com"
}

Copy the value of the parameter endpointAddress into the value of mqtt.host in the config.properties file.

Also change the other properties to the values shown below. Don't forget to save the file.

```
mqtt.port=8883
mqtt.host= {Value of the endpointAddress produced by the above describe-endpoint CLI Command}
mqtt.version=3
client.id.prefix=mydevice
```

#### 12. Pub sub exercise where we can see messages flowing between the device simulator and the IOT core topic over a HTTPS connection.

Navigate to the AWS IOT core service in a browser tab and follow the instructions below :

Right click and open [Subscribe to a IOT topic](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/SubscribeIOTTopic.pdf)

**Publishing from MQTT Client to IOT core:**

Open the mqtt shell by typing the following command :
```
mqtt shell
```
Publishing from MQTT client to IOT core

Connect to IOT core using the following command and then publish the Hello message using the pub command. Press enter after each command :
```
con -i mydevice

pub -t alexa/temperature -m Hello 

```
Follow instructions here to see the message sfomr the MQTT Client published to the IOT core:

Right click and open [See the IOT device message published](https://github.com/aws-samples/data-protection/blob/master/usecase-9/img/SeeIOTDevicePublishedMessage.pdf)

```
type **disconnect** and press enter to Disconnect from the IOT core connection

type exit and press enter to exit out of the MQTT shell
```
**Publishing from IOT core to the MQTT Client:**

Open the mqtt shell by typing the following command :
```
mqtt shell
```
Connect to IOT core using the following command :
```
con -i mydevice

subscribe to the topic monthly_average_temperature by executing the following command :

sub -q 1 -t cloud/monthly_average_temperature -s -oc
```
From the IOT Core console, publish to the topic cloud/monthly_average_temperature 

You should see the message "Hello from the IOT console" on the mqtt client within your Cloud9 environment

####Quiz:####

For re:inforced learning on this topic please take this quiz : [IOT Quiz](https://amazonmr.au1.qualtrics.com/jfe/form/SV_cCiyT40de2DRUHQ)


