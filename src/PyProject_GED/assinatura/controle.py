# -*- coding: utf-8 -*- 

import logging
import sys
import chilkat
import os

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def assinarPFX(self, vCertificado, vSenha, vArquivo):
        try:
            iCertificado = chilkat.CkCert()
            iCertificado.LoadPfxFile(str(vCertificado), str(vSenha))
            iCrypt = chilkat.CkCrypt2()
            iSucesso = iCrypt.UnlockComponent("30-day trial")
            if (iSucesso != True):
                self.getLogger().error('Nao foi possivel assinar PFX: Componente Unlock')
                return iSucesso
                sys.exit()
            iCrypt.SetSigningCert(iCertificado)
            iSucesso = iCrypt.CreateP7S(str(vArquivo), self.obtemCaminhoP7s(vArquivo))
            if (iSucesso == False):
                self.getLogger().error('Nao foi possivel assinar PFX: Criar P7s')
                return iSucesso
                sys.exit()
            iCrypt.SetVerifyCert(iCertificado)
            iSucesso = iCrypt.VerifyP7S(str(vArquivo), self.obtemCaminhoP7s(vArquivo))
            if (iSucesso == False):
                self.getLogger().error('Nao foi possivel assinar PFX: Verificar P7s')
                return iSucesso
                sys.exit()
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel assinar PFX: ' + str(e))
            return False
        
    def verificaP7s(self, vCertificado, vSenha, vArquivo):
        try:
            iCertificado = chilkat.CkCert()
            iCertificado.LoadPfxFile(vCertificado, vSenha)
            iCrypt = chilkat.CkCrypt2()
            iCrypt.SetVerifyCert(iCertificado)
            iSucesso = iCrypt.VerifyP7S(vArquivo, self.obtemCaminhoP7s(vArquivo))
            if (iSucesso == False):
                self.getLogger().error('Nao foi possivel verifica P7s: Verificar P7s')
                return iSucesso
                sys.exit()
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel verificar p7s: ' + str(e))
            return False
        
    def obtemCaminhoP7s(self, vArquivo):
        try:
            iArquivo = os.path.splitext(str(vArquivo))[0] + '.p7s'
            return iArquivo
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtem Caminho p7s: ' + str(e))
            return False