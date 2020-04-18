from unittest import TestCase
import os

from osbot_aws.apis.S3 import S3


class test_setup(TestCase):
    def test_first_one(self):
        print('------checking out secret ---- ')
        print(f'PWD: {os.getenv("PWD")}')
        print(f'PWD: {len(os.getenv("SUPER_SECRET"))}')
        print(f'PWD: {os.getenv("SUPER_SECRET")}')



    def test_second(self):
        s3 = S3()
        print(s3.buckets())

    def test_third(self):
        pass

    def test_third__a(self):
        pass