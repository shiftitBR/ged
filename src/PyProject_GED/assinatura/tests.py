# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django.test                        import TestCase

import sys
import chilkat

class Test(TestCase):
    
    def setUp(self):

        pass
    
    
    def tearDown(self):

        pass
    
    
    def testAssinaturaPFX(self):
        cert = chilkat.CkCert()
        cert.LoadPfxFile("/home/diego/Público/certificados/bradesco.pfx", 'souza029')
        crypt = chilkat.CkCrypt2()
        success = crypt.UnlockComponent("30-day trial")
        if (success != True):
            print crypt.lastErrorText()
            sys.exit()
        crypt.SetSigningCert(cert)
        success = crypt.CreateP7S("/home/diego/Público/teste_assinar.odt","/home/diego/Público/teste_assinar.p7s")
        if (success == False):
            print crypt.lastErrorText()
            sys.exit()
        crypt.SetVerifyCert(cert)
        success = crypt.VerifyP7S("/home/diego/Público/teste_assinar.odt","/home/diego/Público/teste_assinar.p7s")
        if (success == False):
            print crypt.lastErrorText()
            sys.exit()
        
        self.assertEquals(success, True)
        
    def testVerificarAssinatura(self):
        crypt = chilkat.CkCrypt2()
        success = crypt.VerifyP7S("/home/diego/Público/teste_assinar.odt","/home/diego/Público/teste_assinar.p7s")
        self.assertEquals(success, True)
        