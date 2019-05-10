import unittest
import subprocess
import boto3
import os
import time

class TestUseCase5(unittest.TestCase):

    def setUp(self):
        self.ddb_client = boto3.client('dynamodb')
        self.acm_pca_client = boto3.client('acm-pca')
        self.pwd = os.getcwd()

    def test_step1(self):
        print("Test step 1")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-1.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(5)
        try:
            t = self.ddb_client.describe_table(TableName='shared_variables_crypto_builders_usecase_6')
        except self.ddb_client.exceptions.ResourceNotFoundException:
            self.fail("missing ddb table")

    def test_step2(self):
        print("Test step 3")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-2.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(5)
        # TODO:
        # response = self.acm_pca_client.describe_certificate_authority(
        #     CertificateAuthorityArn=subordinate_pca_arn
        # )

    def test_step3(self):
        print("Test step 3")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-3.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(1)
        self.assertEqual(os.path.isfile(self.pwd+'/data-protection/usecase-5/self-signed-cert.pem'), True )

    def test_step4(self):
        print("Test step 4")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-4.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(1)
        self.assertEqual(os.path.isfile(self.pwd+'/data-protection/usecase-5/signed_subordinate_ca_cert.pem'), True )

    def test_step5(self):
        print("Test step 5")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-5.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(1)
        # TODO:
        # validate subordinate_pca_arn

    def test_step6(self):
        print("Test step 6")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-6.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(1)
        # TODO:
        # get ALB
        # validate cert

    def test_step7(self):
        print("Test step 7")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-7.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)

    def test_step8(self):
        print("Test step 8")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-8.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)

    def test_step9(self):
        print("Test step 9")
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-5/usecase-5-step-9-cleanup.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(5)
        self.assertEqual(os.path.isfile(self.pwd+'/data-protection/usecase-5/self-signed-cert.pem'), False )
        self.assertEqual(os.path.isfile(self.pwd+'/data-protection/usecase-5/signed_subordinate_ca_cert.pem'), False )


if __name__ == '__main__':
    unittest.main()
