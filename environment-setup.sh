#!/bin/bash

PACKAGE_NAMES="boto3 aws-encryption-sdk pathlib flask pyopenssl requests"
if [ -z ${TEST_ENVIRONMENT+x} ] || [ "${TEST_ENVIRONMENT}" != "1" ]; then
    PACKAGE_NAMES="${PACKAGE_NAMES} ikpdb"
fi

echo test environment: $TEST_ENVIRONMENT
echo installing python dependencies: $PACKAGE_NAMES

PIPOK=0
OUT=$(sudo pip install -U pip 2>&1)
if [ "$?" == "0" ]; then
    PIPOK=1
else
    echo $OUT > setup.log
    OUT=$(pip install -U pip 2>&1)
    if [ "$?" == "0" ]; then
        PIPOK=1
    else
        echo $OUT > setup.log
    fi
fi

if [ "$PIPOK" == "1" ]; then
    OUT=$(pip install --user ${PACKAGE_NAMES})
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
