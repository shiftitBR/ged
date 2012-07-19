# -*- coding: utf-8 -*- 

import logging
import datetime

from models               import Versao
from models               import Estado_da_Versao
from models               import Tipo_de_Documento
from models               import Documento
from autenticacao.models  import Usuario #@UnresolvedImport  
from seguranca.models     import Pasta   #@UnresolvedImport    
from indice.models        import Indice   #@UnresolvedImport
from objetos_auxiliares   import Documento as DocumentoAuxiliar

from PyProject_GED        import oControle


class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def obtemListaDocumentos(self, vIDPasta):
        try:
            iListaDocumentosAuxiliar=[]
            iListaVersao = Versao.objects.using(oControle.getBanco()).filter(documento__pasta = vIDPasta)
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
                iDocumento.arquivo= iListaVersao[i].arquivo
                iDocumento.estado= iListaVersao[i].estado
                iDocumento.id_estado= iListaVersao[i].estado.id_estado_da_versao
                iDocumento.protocolo= iListaVersao[i].protocolo
                iDocumento.assinado= iListaVersao[i].eh_assinado
                iListaDocumentosAuxiliar.append(iDocumento)
            return iListaDocumentosAuxiliar
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter a lista de documentos: ' + str(e))
            return False
        
    def obtemNomeDaPasta(self, vIDPasta):
        try:
            iPasta = Pasta.objects.using(oControle.getBanco()).filter(id_pasta= vIDPasta)[0]
            return iPasta.nome
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter a lista de documentos: ' + str(e))
            return False
        
    def obtemIDTipoDocumento(self, vDsc_Tipo_Documento):
        try:
            iIDTipo_Documento = Tipo_de_Documento.objects.using(oControle.getBanco()).filter(descricao= vDsc_Tipo_Documento)[0]
            return iIDTipo_Documento
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter o ID do tipo de documento: ' + str(e))
            return False
    
    def obtemListaTipoDocumento(self):
        try:
            iListaTipoDocumento = Tipo_de_Documento.objects.using(oControle.getBanco()).filter()
            return iListaTipoDocumento
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter a lista de tipos de documentos: ' + str(e))
            return False
    
    def obtemListaIndices(self):
        try:
            iListaIndices = Indice.objects.using(oControle.getBanco()).filter()
            return iListaIndices
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter a lista de indices: ' + str(e))
            return False
        
    def obtemUsuario(self, vUsuario):
        try:
            iUsuario= Usuario.objects.using(oControle.getBanco()).filter(pk= vUsuario.pk)[0]
            return iUsuario
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter o Usuario pelo user ' + str(e))
            return False
        
    def salvaDocumento(self, vIDTipo_Doc, vIDResponsavel, vIDPasta, vAssunto, vEh_Publico, vDataValida= str(datetime.datetime.today())[:19],
                            vDataDescarte= str(datetime.datetime.today())[:19]):
        try:
            iPasta          = Pasta.objects.filter(id_pasta= vIDPasta)[0]
            
            iDocumento                  = Documento()
            iDocumento.id_documento     = 1
            iDocumento.tipo_documento   = vIDTipo_Doc
            iDocumento.usr_responsavel  = vIDResponsavel
            iDocumento.pasta            = iPasta
            iDocumento.assunto          = vAssunto
            iDocumento.versao_atual     = 1
            iDocumento.data_validade    = vDataValida
            iDocumento.data_descarte    = vDataDescarte
            iDocumento.eh_pulbico       = vEh_Publico
            iDocumento.save()
            return iDocumento
        except Exception, e:
            self.getLogger().error('Nao foi possivel salvar o Documento: ' + str(e))
            return False
        
    def salvaVersao(self, vIDDocumento, vIDCriador, vIDEstado, vVersao, vArquivo, vProtocolo, 
                    vDataCriacao= str(datetime.datetime.today())[:19], vDsc_Modificacao=None, vEh_Assinado=False):
        try:
            iDocumento  = Documento.objects.filter(id_documento= vIDDocumento)[0]
            iCriador    = Usuario.objects.filter(id= vIDCriador)
            iEstado     = Estado_da_Versao.objects.filter(id_estado_da_versao= vIDEstado)
            
            iVersao                 = Versao()
            iVersao.documento       = iDocumento
            iVersao.usr_criador     = iCriador
            iVersao.estado          = iEstado
            iVersao.versao          = vVersao
            iVersao.dsc_modificacao = vDsc_Modificacao
            iVersao.arquivo         = vArquivo
            iVersao.protocolo       = vProtocolo
            iVersao.data_criacao    = vDataCriacao
            iVersao.eh_assinado     = vEh_Assinado
            iVersao.save()
            return iVersao
        except Exception, e:
            self.getLogger().error('Nao foi possivel salvar a Versao do Documento: ' + str(e))
            return False