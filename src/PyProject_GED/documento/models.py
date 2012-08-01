'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models

from autenticacao.models        import Empresa #@UnresolvedImport
from autenticacao.models        import Usuario #@UnresolvedImport
from seguranca.models           import Pasta #@UnresolvedImport
from multiuploader.models       import MultiuploaderImage #@UnresolvedImport
from objetos_auxiliares         import Documento as DocumentoAuxiliar
from controle                   import Controle as DocumentoControle

import datetime
import logging

#-----------------------------DOCUMENTO----------------------------------------

class Tipo_de_Documento(models.Model):
    id_tipo_documento       = models.IntegerField(max_length=3, primary_key=True)
    descricao               = models.CharField(max_length=30)
    eh_nativo               = models.BooleanField(null= False)
    empresa                 = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_tipo_de_documento'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Tipo_de_Documento.objects.order_by('-id_tipo_documento')) > 0:   
            iUltimoRegistro = Tipo_de_Documento.objects.order_by('-id_tipo_documento')[0] 
            self.id_tipo_documento= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_documento= 1
        super(Tipo_de_Documento, self).save()
    
    def criaTipoDocumento(self, vEmpresa, vDescricao):
        try:
            iTipoDeDocumento= Tipo_de_Documento()
            iTipoDeDocumento.descricao= vDescricao
            iTipoDeDocumento.eh_nativo= True
            iTipoDeDocumento.empresa= vEmpresa
            iTipoDeDocumento.save()
            return iTipoDeDocumento
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os tipos de Documento: ' + str(e))
            return False
    
    def obtemIDTipoDocumento(self, vIDEmpresa, vDsc_Tipo_Documento):
        try:
            iIDTipo_Documento = Tipo_de_Documento.objects.filter(empresa= vIDEmpresa).filter(descricao= vDsc_Tipo_Documento)[0]
            return iIDTipo_Documento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o ID do tipo de documento: ' + str(e))
            return False
    
    def obtemListaTipoDocumento(self, vIDEmpresa):
        try:
            iListaTipoDocumento = Tipo_de_Documento.objects.filter(empresa= vIDEmpresa)
            return iListaTipoDocumento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de tipos de documentos: ' + str(e))
            return False

class Documento(models.Model):
    id_documento    = models.IntegerField(max_length=10, primary_key=True, blank=True)
    tipo_documento  = models.ForeignKey(Tipo_de_Documento, null= False)
    usr_responsavel = models.ForeignKey(Usuario, null= False)
    pasta           = models.ForeignKey(Pasta, null= False)
    assunto         = models.CharField(max_length=100, null= False)
    versao_atual    = models.IntegerField(max_length=3, null= False)
    data_validade   = models.DateTimeField(null= True)
    data_descarte   = models.DateTimeField(null= True)
    eh_publico      = models.BooleanField(null= False)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_documento'
    
    def __unicode__(self):
        return self.assunto
    
    def save(self): 
        if self.id_documento == '' or self.id_documento== None:
            if len(Documento.objects.order_by('-id_documento')) > 0:   
                iUltimoRegistro = Documento.objects.order_by('-id_documento')[0] 
                self.id_documento= iUltimoRegistro.pk + 1
            else:
                self.id_documento= 1
        super(Documento, self).save()  
    
    def salvaDocumento(self, vIDEmpresa, vIDTipo_Doc, vIDPasta, vAssunto, vEh_Publico, vResponsavel,
                       vDataValida= None, vDataDescarte= None):
        try:
            iPasta          = Pasta.objects.filter(id_pasta= vIDPasta)[0]
            iTipoDoc        = Tipo_de_Documento.objects.filter(id_tipo_documento= vIDTipo_Doc)[0]
            iEmpresa        = Empresa.objects.filter(id_empresa= vIDEmpresa)[0]
            
            iDocumento                  = Documento()
            iDocumento.empresa          = iEmpresa
            iDocumento.tipo_documento   = iTipoDoc
            iDocumento.usr_responsavel  = vResponsavel
            iDocumento.pasta            = iPasta
            iDocumento.assunto          = vAssunto
            iDocumento.versao_atual     = 1
            iDocumento.data_validade    = vDataValida
            iDocumento.data_descarte    = vDataDescarte
            iDocumento.eh_pulbico       = vEh_Publico
            iDocumento.save()
            return iDocumento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar o Documento: ' + str(e))
            return False 

#-----------------------------VERSAO----------------------------------------
        
class Estado_da_Versao(models.Model):
    id_estado_da_versao = models.IntegerField(max_length=3, primary_key=True)
    descricao           = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_estado_da_versao'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Estado_da_Versao.objects.order_by('-id_estado_da_versao')) > 0:   
            iUltimoRegistro = Estado_da_Versao.objects.order_by('-id_estado_da_versao')[0] 
            self.id_estado_da_versao= iUltimoRegistro.pk + 1
        else:
            self.id_estado_da_versao= 1
        super(Estado_da_Versao, self).save()
        
    def criaEstadoVersao(self, vDescricao):
        try:
            iEstadoVersao = Estado_da_Versao(descricao= vDescricao)
            iEstadoVersao.save()
            return iEstadoVersao
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar o estado da versao: ' + str(e))
            return False


        
class Versao(models.Model):
    id_versao       = models.IntegerField(max_length=10, primary_key=True, blank=True)
    documento       = models.ForeignKey(Documento, null= False)
    usr_criador     = models.ForeignKey(Usuario, null= False)
    estado          = models.ForeignKey(Estado_da_Versao, null= False)
    versao          = models.IntegerField(max_length=3, null= False)
    dsc_modificacao = models.CharField(max_length=200, null= True)
    upload          = models.ForeignKey(MultiuploaderImage, null= False)
    protocolo       = models.CharField(max_length=20, null=True)
    data_criacao    = models.DateTimeField(null= False)
    eh_assinado     = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_versao'
    
    def __unicode__(self):
        return str(self.id_versao)
    
    def save(self): 
        if self.id_versao == '' or self.id_versao == None:
            if len(Versao.objects.order_by('-id_versao')) > 0:   
                iUltimoRegistro = Versao.objects.order_by('-id_versao')[0] 
                self.id_versao= iUltimoRegistro.pk + 1
            else:
                self.id_versao= 1
        super(Versao, self).save()   
        
    def obtemListaDocumentos(self, vIDEmpresa, vIDPasta):
        try:
            iListaDocumentosAuxiliar=[]
            iListaVersao = Versao.objects.filter(documento__empresa= vIDEmpresa).filter(documento__pasta = vIDPasta)
            for i in range(len(iListaVersao)):    
                iDocumento= DocumentoAuxiliar()
                iDocumento.id= iListaVersao[i].documento.id_documento
                iDocumento.id_versao= iListaVersao[i].id_versao
                iDocumento.assunto= iListaVersao[i].documento.assunto
                iDocumento.pasta= iListaVersao[i].documento.pasta
                iDocumento.id_pasta= iListaVersao[i].documento.pasta.id_pasta
                iDocumento.tipo_documento= iListaVersao[i].documento.tipo_documento
                iDocumento.id_tipo_documento= iListaVersao[i].documento.tipo_documento.id_tipo_documento
                iDocumento.versao_atual= iListaVersao[i].documento.versao_atual
                iDocumento.publico= iListaVersao[i].documento.eh_publico
                iDocumento.responsavel= iListaVersao[i].documento.usr_responsavel
                iDocumento.id_responsavel= iListaVersao[i].documento.usr_responsavel.id
                iDocumento.descarte= iListaVersao[i].documento.data_descarte
                iDocumento.validade= iListaVersao[i].documento.data_validade
                iDocumento.data_criacao= iListaVersao[i].data_criacao
                iDocumento.num_versao= iListaVersao[i].versao
                iDocumento.descricao= iListaVersao[i].dsc_modificacao
                iDocumento.criador= iListaVersao[i].usr_criador
                iDocumento.id_criador= iListaVersao[i].usr_criador.id
                iDocumento.arquivo= str(iListaVersao[i].upload.image)
                iDocumento.estado= iListaVersao[i].estado
                iDocumento.id_estado= iListaVersao[i].estado.id_estado_da_versao
                iDocumento.protocolo= iListaVersao[i].protocolo
                iDocumento.assinado= iListaVersao[i].eh_assinado
                iDocumento.visualizavel= DocumentoControle().ehVisualizavel(str(iListaVersao[i].upload.filename))
                iListaDocumentosAuxiliar.append(iDocumento)
            return iListaDocumentosAuxiliar
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de documentos: ' + str(e))
            return False
    
    def obtemCaminhoArquivo(self, vIDVersao):
        try:
            iVersao = Versao.objects.filter(id_versao = vIDVersao)[0]
            return iVersao.upload.image
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o Usuario pelo user ' + str(e))
            return False
        
    def alterarEstadoVersao(self, vIDVersao, vIDEstado):
        try:
            iEstadoVersao= Estado_da_Versao.objects.filter(id_estado_da_versao= vIDEstado)[0]
            iVersao = Versao.objects.filter(id_versao = vIDVersao)[0]
            iVersao.estado= iEstadoVersao
            iVersao.save()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel alterarEstadoVersao ' + str(e))
            return False
    
    def salvaVersao(self, vIDDocumento, vIDCriador, vIDEstado, vVersao, vUpload, vProtocolo, 
                    vDataCriacao= str(datetime.datetime.today())[:19], vDsc_Modificacao=None, vEh_Assinado=False):
        try:
            iDocumento  = Documento.objects.filter(id_documento= vIDDocumento)[0]
            iCriador    = Usuario.objects.filter(id= vIDCriador)[0]
            iEstado     = Estado_da_Versao.objects.filter(id_estado_da_versao= vIDEstado)[0]
            iUpload     = MultiuploaderImage.objects.filter(key_data = vUpload)[0]

            iVersao                 = Versao()
            iVersao.documento       = iDocumento
            iVersao.usr_criador     = iCriador
            iVersao.estado          = iEstado
            iVersao.versao          = vVersao
            iVersao.dsc_modificacao = vDsc_Modificacao
            iVersao.upload          = iUpload
            iVersao.protocolo       = vProtocolo
            iVersao.data_criacao    = vDataCriacao
            iVersao.eh_assinado     = vEh_Assinado
            iVersao.save()
            return iVersao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar a Versao do Documento: ' + str(e))
            return False
