'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.documento.models     import Versao
from objetos_auxiliares                 import infoAss
from controle                           import Controle as AssinaturaControle

import logging
import sys
import chilkat

class Certificado(models.Model):
    arquivo = models.FileField(upload_to='documentos/certificados/', max_length=300)
    
    class Meta:
        db_table= 'tb_certificado'
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        
    def __unicode__(self):
        return str(self.arquivo)
    
class Assinatura(models.Model):
    id_assinatura       = models.IntegerField(max_length=10, primary_key=True, blank=True)
    usuario             = models.ForeignKey(Usuario, null= False)
    versao              = models.ForeignKey(Versao, null= False)
    arquivo             = models.FileField(upload_to='documentos/certificados/', max_length=300)
    
    class Meta:
        db_table= 'tb_assinatura'
        verbose_name = 'Assinatura    '
        verbose_name_plural = 'Assinaturas'
        
    def __unicode__(self):
        return str(self.arquivo)
    
    def save(self): 
        if self.id_assinatura == '' or self.id_assinatura== None:
            if len(Assinatura.objects.order_by('-id_assinatura')) > 0:   
                iUltimoRegistro = Assinatura.objects.order_by('-id_assinatura')[0] 
                self.id_assinatura= iUltimoRegistro.pk + 1
            else:
                self.id_assinatura= 1
            
        super(Assinatura, self).save() 
        
    def salvaAssinatura(self, vUsuario, vVersao, vArquivo):
        try:
            iAssinatura = Assinatura()
            iAssinatura.usuario = vUsuario
            iAssinatura.versao  = vVersao
            iAssinatura.arquivo = vArquivo
            iAssinatura.save()
            return iAssinatura
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar Assinatura: ' + str(e))
            return False 
        
    def assinaDocumento(self, vCertificado, vSenha, vUsuario, vVersao):
        try:
            iArquivo     = vVersao.upload.image
            iNumero      = self.obtemNrAssDaVersao(vVersao)
            iCaminhoP7s  = AssinaturaControle().obtemCaminhoP7s(iArquivo, vUsuario.empresa.id_empresa, vVersao.documento.pasta, iNumero)
            iCertificado = chilkat.CkCert()
            iCertificado.LoadPfxFile(str(vCertificado), str(vSenha))
            iCrypt = chilkat.CkCrypt2()
            iSucesso = iCrypt.UnlockComponent("30-day trial")
            if (iSucesso != True):
                logging.getLogger().error('Nao foi possivel assinar PFX: Componente Unlock')
                return iSucesso
                sys.exit()
            iCrypt.SetSigningCert(iCertificado)
            iSucesso = iCrypt.CreateP7S(str(iArquivo), iCaminhoP7s)
            if (iSucesso == False):
                logging.getLogger().error('Nao foi possivel assinar PFX: Criar P7s' + iCrypt.lastErrorText())
                return iSucesso
                sys.exit()
            iCrypt.SetVerifyCert(iCertificado)
            iSucesso = iCrypt.VerifyP7S(str(iArquivo), iCaminhoP7s)
            if (iSucesso == False):
                logging.getLogger().error('Nao foi possivel assinar PFX: Verificar P7s' + iCrypt.lastErrorText())
                return iSucesso
                sys.exit()
            return self.salvaAssinatura(vUsuario, vVersao, iCaminhoP7s)
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar assina Documento: ' + str(e))
            return False 
        
    def obtemNrAssDaVersao(self, vVersao):
        try:
            iAssinaturas = Assinatura.objects.filter(versao=vVersao)
            return len(iAssinaturas)
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem Nr Ass Da Versaoa: ' + str(e))
            return False 
        
    def obtemListaAssDaVersao(self, vVersao):
        try:
            iAssinaturas = Assinatura.objects.filter(versao=vVersao)
            return iAssinaturas
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem Lista Ass Da Versao: ' + str(e))
            return False 
        
    def obtemListaInfoAss(self, vVersao):
        try:
            iAssinaturas    = Assinatura.objects.filter(versao__documento=vVersao.documento).order_by('-id_assinatura')
            iListaInfo      = []
            iInfoCert       = chilkat.CkString()
            iCert           = chilkat.CkCert()
            iSeq= 0
            for iAssinatura in iAssinaturas:
                iCert.LoadFromFile(str(iAssinatura.arquivo))
                iInfo       = infoAss()
                iSeq                = iSeq+1
                iInfo.seq           = iSeq
                iInfo.num_versao    = iAssinatura.versao.versao
                iCert.get_SubjectO(iInfoCert)
                iInfo.organizacao   = iInfoCert.getUtf8()
                iCert.get_SubjectCN(iInfoCert)
                iInfo.nome          = iInfoCert.getUtf8()
                iCert.get_SubjectL(iInfoCert)
                iInfo.local         = iInfoCert.getUtf8()
                iInfo.idVersao      = iAssinatura.versao.id_versao
                iCert.get_SubjectE(iInfoCert)
                iInfo.email         = iInfoCert.getUtf8()
                iListaInfo.append(iInfo)
            return iListaInfo
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem Lista Info Ass: ' + str(e))
            return False 