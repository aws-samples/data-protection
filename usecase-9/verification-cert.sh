#!/bin/bash

export CSR_FILE=verification_cert.csr
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export BUCKET=certificate-holder-${ACCOUNT}
export SPLIT='/-----BEGIN CERTIFICATE-----/'
export END_CERT='-----END CERTIFICATE-----'
export PWD=$(pwd)

# get subordinate CA Arn
SUB_ARN=$(aws acm-pca list-certificate-authorities --max-results 10 | jq -r '.CertificateAuthorities[] | .Type, .Arn' | grep SUBORDINATE -A 1 | sed 'N;s/SUBORDINATE\n//')

# issue cert 
CERT_ARN=$(aws acm-pca issue-certificate --certificate-authority-arn ${SUB_ARN} --csr file://./${CSR_FILE} --signing-algorithm SHA256WITHRSA --validity "Value=50,Type=DAYS" --output json | jq -r .CertificateArn)

# wait for async issue-certficate operation to finish 
aws acm-pca wait certificate-issued --certificate-authority-arn ${SUB_ARN} --certificate-arn ${CERT_ARN}

# retrieve cert chain & extract first entry in chain
aws acm-pca get-certificate --certificate-authority-arn ${SUB_ARN} --certificate-arn ${CERT_ARN} --output text | csplit -z -f /tmp/cert- - "${SPLIT}" '{*}'
echo ${END_CERT} >> /tmp/cert-00
mv /tmp/cert-00 ${PWD}/verification_cert.pem

# copy signed cert to s3
aws s3 cp ${PWD}/verification_cert.pem s3://${BUCKET}/verification_cert.pem

# export sub CA cert
aws acm-pca get-certificate-authority-certificate --certificate-authority-arn ${SUB_ARN} --output text | csplit -z -f /tmp/cert- - "${SPLIT}" '{*}'
echo ${END_CERT} >> /tmp/cert-00
mv /tmp/cert-00 ${PWD}/subordinate_ca_cert.pem

# copy sub CA cert to s3
aws s3 cp ${PWD}/subordinate_ca_cert.pem s3://${BUCKET}/subordinate_ca_cert.pem

# clean up 
rm /tmp/cert-??
