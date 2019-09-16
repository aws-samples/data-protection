#!/bin/bash

alias python='python36'
PIP3=pip-3.6
alias pip='$(PIP3)'
T=$(date)

PACKAGE_NAMES="boto3 aws-encryption-sdk pathlib flask pyopenssl requests"
if [ -z ${TEST_ENVIRONMENT+x} ] || [ "${TEST_ENVIRONMENT}" != "1" ]; then
    PACKAGE_NAMES="${PACKAGE_NAMES} ikp3db"
fi

echo installing python dependencies: $PACKAGE_NAMES
echo $T > setup.log

PIPOK=0
OUT=$(sudo /usr/bin/$PIP3 install -U pip 2>&1) # FIX!
if [ "$?" == "0" ]; then
    PIPOK=1
else
    echo $OUT >> setup.log
    OUT=$(pip install -U pip 2>&1)
    if [ "$?" == "0" ]; then
        PIPOK=1
    else
        echo $OUT >> setup.log
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

