# -*- coding: utf-8 -*- 

import logging

from models               import Versao
from seguranca.models     import Pasta   #@UnresolvedImport    
from objetos_auxiliares   import Documento as DocumentoAuxiliar

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def obtemListaDocumentos(self, vIDPasta):
        try:
            iListaDocumentosAuxiliar=[]
            iListaVersao = Versao.objects.filter(documento__pasta= vIDPasta)
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
                iDocumento.id_responsavel= iListaVersao[i].id_documento.usr_responsavel.id_usuario
                iDocumento.descarte= iListaVersao[i].documento.data_descarte
                iDocumento.validade= iListaVersao[i].documento.data_validade
                iDocumento.data_criacao= iListaVersao[i].data_criacao
                iDocumento.num_versao= iListaVersao[i].versao
                iDocumento.descricao= iListaVersao[i].dsc_modificacao
                iDocumento.criador= iListaVersao[i].usr_criador
                iDocumento.id_criador= iListaVersao[i].usr_criador.id_usuario
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
            iPasta = Pasta.objects.filter(id_pasta= vIDPasta)[0]
            return iPasta.nome
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter a lista de documentos: ' + str(e))
            return False