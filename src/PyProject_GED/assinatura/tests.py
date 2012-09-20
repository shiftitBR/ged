# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django.test                            import TestCase
from django.conf                            import settings

import sys
import chilkat

class Test(TestCase):
    
    def setUp(self):

        pass
    
    
    def tearDown(self):

        pass
    
    
    def testAssinaturaPFX(self):
        cert = chilkat.CkCert()
        iCertificado = '%s/media_teste/sample.pfx' % settings.MEDIA_ROOT
        cert.LoadPfxFile(iCertificado, 'sample')
        crypt = chilkat.CkCrypt2()
        success = crypt.UnlockComponent("30-day trial")
        if (success != True):
            print crypt.lastErrorText()
            sys.exit()
        crypt.SetSigningCert(cert)
        iArquivo = '%s/media_teste/texto.odt' % settings.MEDIA_ROOT
        success = crypt.CreateP7S(iArquivo, '%s/media_teste/teste_assinar.p7s' % settings.MEDIA_ROOT)
        if (success == False):
            print crypt.lastErrorText()
            sys.exit()
        crypt.SetVerifyCert(cert)
        success = crypt.VerifyP7S(iArquivo, '%s/media_teste/teste_assinar.p7s' % settings.MEDIA_ROOT)
        if (success == False):
            print crypt.lastErrorText()
            sys.exit()
        
        self.assertEquals(success, True)
        
    def testVerificarAssinatura(self):
        crypt = chilkat.CkCrypt2()
        success = crypt.VerifyP7S('%s/media_teste/texto.odt' % settings.MEDIA_ROOT,'%s/media_teste/teste_assinar.p7s' % settings.MEDIA_ROOT)
        self.assertEquals(success, True)
        