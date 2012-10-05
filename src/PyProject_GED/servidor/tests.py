'''
Created on Oct 5, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.test                                import TestCase
from PyProject_GED.servidor.models import Servidor


class Test(TestCase):
    
    def setUp(self):
        pass
    
    
    def tearDown(self):
        pass

    def testaSocket(self):
        Servidor().iniciaSocket_TCP()