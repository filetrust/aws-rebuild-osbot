from unittest import TestCase
import os

class test_setup(TestCase):
    def test_first_one(self):
        print('------checking out secret ---- ')
        print(f'PWD: {os.getenv("PWD")}')
        print(f'PWD: {os.getenv("SUPER_SECRET")}')



    def test_second(self):
        print('here')

    def test_third(self):
        pass

    def test_third__a(self):
        pass