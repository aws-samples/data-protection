#!/bin/bash

T=$(date)

PYTHON_PACKAGES="aws-encryption-sdk pathlib flask pyopenssl requests cryptography"
if [ -z ${TEST_ENVIRONMENT+x} ] || [ "${TEST_ENVIRONMENT}" != "1" ]; then
    PYTHON_PACKAGES="${PACKAGE_NAMES} ikp3db"
fi

echo configuring python environment, please wait...
echo $T > setup.log
sudo rm -rf /root/.cache/pip 2>&1 >> setup.log
sudo python -m pip install --upgrade pip 2>&1 >> setup.log
#sudo python -m pip uninstall -y aws-sam-cli 2>&1 >> setup.log
sudo python -m pip install --upgrade boto3 awscli 2>&1 >> setup.log
python -m pip install --user ${PYTHON_PACKAGES} 2>&1 >> setup.log
echo python setup complete

T=$(date)
echo $T >> setup.log
echo environment setup complete