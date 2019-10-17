#!/bin/bash

T=$(date)

PACKAGE_NAMES="boto3 aws-encryption-sdk pathlib flask pyopenssl requests"
if [ -z ${TEST_ENVIRONMENT+x} ] || [ "${TEST_ENVIRONMENT}" != "1" ]; then
    PACKAGE_NAMES="${PACKAGE_NAMES} ikp3db"
fi

echo installing python dependencies: $PACKAGE_NAMES
echo $T > setup.log

PIPOK=0
echo "upgrading pip (sudo)" >> setup.log
OUT=$(sudo /usr/bin/pip-3.6 install --upgrade pip 2>&1) # FIX!
if [ "$?" == "0" ]; then
    PIPOK=1
else
    echo $OUT >> setup.log
    echo "upgrading pip (user)" >> setup.log
    OUT=$(pip-3.6 install ---upgrade pip 2>&1)
    if [ "$?" == "0" ]; then
        PIPOK=1
    else
        echo $OUT >> setup.log
    fi
fi

if [ "$PIPOK" == "1" ]; then
    echo "calling pip install" >> setup.log
    OUT=$(python36 -m pip install --user ${PACKAGE_NAMES})
    if [ "$?" == "0" ]; then
        echo "SUCCESS: installed python dependencies ${PACKAGE_NAMES}" > ok
        cat ok
        exit 0
    else
        echo ERROR: failed to install python dependencies
        echo $OUT >> setup.log
        exit 1
    fi
else
    echo ERROR: failed to upgrade pip
    exit 2
fi

