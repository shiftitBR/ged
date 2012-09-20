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
        print '>>>>>>>>>>>>>>>>>>>>>>> testAssinaturaPFX'
        cert = chilkat.CkCert()
        cert.LoadPfxFile("/home/diego/Público/certificados/sample.pfx", 'sample')
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
        print crypt.lastErrorText()
        crypt.SetVerifyCert(cert)
        success = crypt.VerifyP7S("/home/diego/Público/teste_assinar.odt","/home/diego/Público/teste_assinar.p7s")
        if (success == False):
            print crypt.lastErrorText()
            sys.exit()
        self.assertEquals(success, True)
        
    def testAssinaturaCRT(self):
        print '>>>>>>>>>>>>>>>>>>>>>>> testAssinaturaCRT'
        
        cert = chilkat.CkCert()

        #  Load the cert from a PEM file;
        cert.LoadPfxFile("/home/diego/Público/certificados/sample.pfx", 'sample')
        print '>>>>>>>>>>>>>>>>>>>>>>> 01'
              
        #pkey = chilkat.CkPrivateKey()
        #print '>>>>>>>>>>>>>>>>>>>>>>> 02'
        
        #  Load the private key from an RSA PEM file:
        #success = pkey.SavePkcs8File("/home/diego/Público/certificados/certificado.pfx")
        #print '>>>>>>>>>>>>>>>>>>>>>>> 03'
        #print success
        #if (success != True):
        #    print cert.lastErrorText()
        #    sys.exit()
        
        #  Use Chilkat Crypt (a non-freeware component) to create
        #  a digital signature using the certificate w/ private key:
        crypt = chilkat.CkCrypt2()
        print '>>>>>>>>>>>>>>>>>>>>>>> 04'
        
        #  Any string argument automatically begins the 30-day trial.
        success = crypt.UnlockComponent("30-day trial")
        print '>>>>>>>>>>>>>>>>>>>>>>> 05'
        print success
        if (success != True):
            print crypt.lastErrorText()
            sys.exit()
        
        #  Tell the crypt component to use this cert.
        crypt.SetSigningCert(cert)
        print '>>>>>>>>>>>>>>>>>>>>>>> 06'
        
        #  A PKCS7 signature for any type of file content can be created:
        success = crypt.CreateP7S("/home/diego/Público/teste_assinar.odt","/home/diego/Público/teste_assinar.p7s")
        print '>>>>>>>>>>>>>>>>>>>>>>> 07'
        print success
        if (success == False):
            print crypt.lastErrorText()
            sys.exit()
        
        print crypt.lastErrorText()
        
        #  Verify and restore the original file:
        crypt.SetVerifyCert(cert)
        print '>>>>>>>>>>>>>>>>>>>>>>> 08'
        
        success = crypt.VerifyP7S("/home/diego/Público/teste_assinar.odt","/home/diego/Público/teste_assinar.p7s")
        if (success == False):
            print crypt.lastErrorText()
            sys.exit()
        
        self.assertEquals(success, True)
        
    def testVerificarAssinatura(self):
        crypt = chilkat.CkCrypt2()
        success = crypt.VerifyP7S("/home/diego/Público/teste_assinar.odt","/home/diego/Público/teste_assinar.p7s")
        self.assertEquals(success, True)