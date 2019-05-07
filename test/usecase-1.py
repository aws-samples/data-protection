import unittest
import subprocess
import boto3
import os
import time

class TestUseCase1(unittest.TestCase):

    def setUp(self):
        self.kms_client = boto3.client('kms')
        self.pwd = os.getcwd()
        
    def test_step1(self):
        
        print(self.pwd)
        child = subprocess.Popen(['python3', self.pwd+'/data-protection/usecase-1/kms_key_creation-Step-1.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        kmsAlias = False
        i = 0
        data = alias = self.kms_client.list_aliases()
        while ( i < len(data['Aliases']) and not(kmsAlias)):
            kmsAlias = data['Aliases'][i]['AliasName'] == 'alias/kms_key_sse_usecase_1'
            i=i+1
        self.assertEqual(kmsAlias, True) # consider alias sufficient validation (for now)

    def test_step2(self):
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-1/usecase-1-Step-2.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        self.assertEqual(os.path.isfile(self.pwd+'/data-protection/usecase-1/plaintext_cycled_u.txt'), True )

    def test_step3(self):
        child = subprocess.Popen(['python', self.pwd+'/data-protection/usecase-1/usecase-1-cleanup-Step-3.py'])
        output = child.communicate()[0]
        self.assertEqual(child.returncode, 0)
        time.sleep(5)
        self.assertEqual(os.path.isfile(self.pwd+'/data-protection/usecase-1/plaintext_cycled_u.txt'), False )
        kmsAlias = False
        i = 0
        data = alias = self.kms_client.list_aliases()
        while ( i < len(data['Aliases']) and not(kmsAlias)):
            kmsAlias = data['Aliases'][i]['AliasName'] == 'alias/kms_key_sse_usecase_1'
            i=i+1
        self.assertEqual(kmsAlias, False) # consider alias sufficient validation (for now)

if __name__ == '__main__':
    unittest.main()
