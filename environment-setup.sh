#!/bin/bash

T=$(date)

PACKAGE_NAMES="aws-encryption-sdk pathlib flask pyopenssl requests"
if [ -z ${TEST_ENVIRONMENT+x} ] || [ "${TEST_ENVIRONMENT}" != "1" ]; then
    PACKAGE_NAMES="${PACKAGE_NAMES} ikp3db"
fi

echo configuring python environment, please wait...
echo $T > setup.log
sudo rm -rf /root/.cache/pip 2>&1 >> setup.log
sudo python -m pip install --upgrade pip 2>&1 >> setup.log
sudo python -m pip uninstall -y aws-sam-cli 2>&1 >> setup.log
sudo python -m pip install --upgrade boto3 awscli 2>&1 >> setup.log
python -m pip install --user ${PACKAGE_NAMES} 2>&1 >> setup.log
echo setup complete