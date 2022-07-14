#!/bin/bash

export MQTT_RPM_URL=https://github.com/hivemq/mqtt-cli/releases/download/v1.2.0/mqtt-cli-1.2.0.noarch.rpm
export PWD=$(pwd)
T=$(date)

PYTHON_PACKAGES="aws-encryption-sdk pathlib flask pyopenssl cryptography"
if [ -z ${TEST_ENVIRONMENT+x} ] || [ "${TEST_ENVIRONMENT}" != "1" ]; then
    PYTHON_PACKAGES="${PACKAGE_NAMES} ikp3db"
fi

echo configuring python environment, please wait...
echo $T > setup.log
sudo rm -rf /root/.cache/pip 2>&1 >> setup.log
sudo python -m pip install --upgrade pip 2>&1 >> setup.log
sudo python -m pip uninstall -y aws-sam-cli 2>&1 >> setup.log
sudo python -m pip install --upgrade boto3 awscli 2>&1 >> setup.log
python -m pip install --user ${PYTHON_PACKAGES} 2>&1 >> setup.log
echo python setup complete

echo installing other tools
T=$(date)
echo $T >> setup.log
sudo rpm --import https://yum.corretto.aws/corretto.key 2>&1 >> setup.log
sudo curl -L -o /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo 2>&1 >> setup.log
sudo yum update -y 2>&1 >> setup.log
sudo yum install -y java-11-amazon-corretto-devel jq csplit ${MQTT_RPM_URL} 2>&1 >> setup.log
mqtt --version 2>&1 >> setup.log # generates ~/.mqtt/config.properties
npm install -g c9 2>&1 >> setup.log

echo downloading Amazon CA public certificate
T=$(date)
echo $T >> setup.log
wget https://www.amazontrust.com/repository/AmazonRootCA1.pem 2>&1 >> setup.log

echo set mqtt properties
echo auth.server.cafile=/home/ec2-user/environment/data-protection/usecase-9/AmazonRootCA1.pem >>  ~/.mqtt-cli/config.properties
echo auth.client.key=/home/ec2-user/environment/data-protection/usecase-9/device_cert.key >>  ~/.mqtt-cli/config.properties
echo auth.client.cert=/home/ec2-user/environment/data-protection/usecase-9/device_cert.pem >>  ~/.mqtt-cli/config.properties

T=$(date)
echo $T >> setup.log
echo environment setup complete
