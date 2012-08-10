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
from objetos_auxiliares         import Versoes as VersaoAuxiliar
from controle                   import Controle as DocumentoControle
from django.db.models           import get_model

import datetime
import logging
import constantes#@UnresolvedImport

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
    
    def obtemListaTipoDocumentoDaEmpresa(self, vIDEmpresa):
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
            iDocumento.data_validade    = vDataValida
            iDocumento.data_descarte    = vDataDescarte
            iDocumento.eh_pulbico       = vEh_Publico
            iDocumento.save()
            return iDocumento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar o Documento: ' + str(e))
            return False 
    
    def obtemInformacoesDocumento(self, vIDVersao):
        try: 
            mHistorico= get_model('historico', 'Historico')
            iVersao = Versao.objects.filter(id_versao= vIDVersao)[0]
            iResponsavel= iVersao.documento.usr_responsavel
            iNomeResponsavel= iResponsavel.first_name + ' ' + iResponsavel.last_name 
            iDocumento= DocumentoAuxiliar()
            iDocumento.idDocumento      = iVersao.documento.id_documento
            iDocumento.assunto          = iVersao.documento.assunto
            iDocumento.dscTipoDoc       = iVersao.documento.tipo_documento.descricao
            iDocumento.nomeResponsavel  = iNomeResponsavel
            iDocumento.nomePasta        = iVersao.documento.pasta.nome
            iDocumento.dataValidade     = iVersao.documento.data_validade
            iDocumento.dataDescarte     = iVersao.documento.data_descarte
            iDocumento.ehPublico        = iVersao.documento.eh_publico
            iDocumento.totalDownloads   = mHistorico().calculaQuantidadeDeDownloadsDoDocumento(iVersao)
            iDocumento.totalVisualizacao= mHistorico().calculaQuantidadeDeVisualizacoesDoDocumento(iVersao)
            
            return iDocumento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemInformacoesDocumento: ' + str(e))
            return False 
        
    def gerarProtocolo(self, vIDDocumento, vNum_versao):
        try:
            iDocumento  = Documento.objects.filter(id_documento= vIDDocumento)[0]
            iDocumento  = str('%07d'%iDocumento.empresa.id_empresa)
            iVersao     = str('%03d'%vNum_versao)
            iProtocolo  = '%s%s' %(iDocumento, iVersao)
            return iProtocolo
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel gerarProtocolo ' + str(e))
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
    
    def obtemEstadosDaVersao(self):
        try:
            iListaEstados = Estado_da_Versao.objects.all()
            return iListaEstados
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter os estados da versao: ' + str(e))
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
    eh_versao_atual = models.BooleanField(null= False)
    
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
        

    def obtemDocumentoAuxiliar(self, vVersao):
        iDocumento = DocumentoAuxiliar()
        iDocumento.id = vVersao.documento.id_documento
        iDocumento.id_versao = vVersao.id_versao
        iDocumento.assunto = vVersao.documento.assunto
        iDocumento.pasta = vVersao.documento.pasta
        iDocumento.id_pasta = vVersao.documento.pasta.id_pasta
        iDocumento.tipo_documento = vVersao.documento.tipo_documento
        iDocumento.id_tipo_documento = vVersao.documento.tipo_documento.id_tipo_documento
        iDocumento.versao_atual = vVersao.eh_versao_atual
        iDocumento.publico = vVersao.documento.eh_publico
        iDocumento.responsavel = vVersao.documento.usr_responsavel
        iDocumento.id_responsavel = vVersao.documento.usr_responsavel.id
        iDocumento.descarte = vVersao.documento.data_descarte
        iDocumento.validade = vVersao.documento.data_validade
        iDocumento.data_criacao = vVersao.data_criacao
        iDocumento.num_versao = vVersao.versao
        iDocumento.descricao = vVersao.dsc_modificacao
        iDocumento.criador = vVersao.usr_criador
        iDocumento.id_criador = vVersao.usr_criador.id
        iDocumento.arquivo = str(vVersao.upload.image)
        iDocumento.estado = vVersao.estado
        iDocumento.id_estado = vVersao.estado.id_estado_da_versao
        iDocumento.protocolo = vVersao.protocolo
        iDocumento.assinado = vVersao.eh_assinado
        iDocumento.nomeArquivo= vVersao.upload.filename.encode('utf-8')
        iDocumento.tipoVisualizacao = DocumentoControle().tipoVisualizavel(vVersao.upload.filename.encode('utf-8'))
        iDocumento.caminhoVisualizar = DocumentoControle().obtemCaminhoVisualizar(str(vVersao.upload.image))
        return iDocumento

    def obtemListaDeDocumentosDaPasta(self, vIDEmpresa, vIDPasta):
        try:
            iListaDocumentosAuxiliar=[]
            iListaVersao = Versao.objects.filter(documento__empresa= vIDEmpresa).filter(
                                    documento__pasta = vIDPasta).filter(eh_versao_atual=True).order_by('-data_criacao')
            for i in range(len(iListaVersao)):    
                iDocumento = self.obtemDocumentoAuxiliar(iListaVersao[i])
                iListaDocumentosAuxiliar.append(iDocumento)
            return iListaDocumentosAuxiliar
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de documentos: ' + str(e))
            return False
    
    def obtemListaDeVersoesDoDocumento(self, vIDVersao):
        try: 
            iVersaoDoc  = Versao.objects.filter(id_versao= vIDVersao)[0]
            iListaVersao= Versao.objects.filter(documento= iVersaoDoc.documento).order_by('versao')
            iLista      = []
            for i in range(len(iListaVersao)):
                iVersao= iListaVersao[i]
                iCriador= iVersao.usr_criador
                iNomeCriador= iCriador.first_name + ' ' + iCriador.last_name 
                iVersaoAux= VersaoAuxiliar()
                iVersaoAux.idVersao        = iVersao.id_versao
                iVersaoAux.num_versao      = iVersao.versao
                iVersaoAux.dsc_modificacao = iVersao.dsc_modificacao
                iVersaoAux.nomeCriador     = iNomeCriador
                iVersaoAux.nomeArquivo     = iVersao.upload.filename.encode('utf-8')
                iVersaoAux.estado          = iVersao.estado.descricao
                iVersaoAux.idEstado        = iVersao.estado.id_estado_da_versao
                iVersaoAux.protocolo       = iVersao.protocolo
                iVersaoAux.ehAssinado      = iVersao.eh_assinado
                iVersaoAux.dataCriacao     = iVersao.data_criacao
                iVersaoAux.eh_versao_atual = iVersao.eh_versao_atual
                iLista.append(iVersaoAux)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaDeVersoesDoDocumento: ' + str(e))
            return False 
    
    def obtemCaminhoArquivo(self, vIDVersao):
        try:
            iVersao = Versao.objects.filter(id_versao = vIDVersao)[0]
            return iVersao.upload.image
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o Usuario pelo user ' + str(e))
            return False
    
    def obtemVersaoAtualDoDocumento(self, vDocumento):
        try:
            iVersao = Versao.objects.filter(documento= vDocumento).filter(eh_versao_atual= True)[0]
            return iVersao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a versao atual do documento ' + str(e))
            return False
        
    def obtemVersao(self, vIDVersao):
        try:
            iVersao = Versao.objects.filter(id_versao = vIDVersao)[0]
            return iVersao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o Usuario pelo user ' + str(e))
            return False
    
    def obsoletarVersao(self, vVersao):
        try:
            iEstado = Estado_da_Versao.objects.filter(id_estado_da_versao= constantes.cntEstadoVersaoObsoleto)[0]
            vVersao.eh_versao_atual= False
            vVersao.estado= iEstado
            vVersao.save()
            return True
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
    
    def salvaVersao(self, vIDDocumento, vIDCriador, vIDEstado, vVersao, vUploadKeyData, vProtocolo, 
                    vDataCriacao= str(datetime.datetime.today())[:19], vDsc_Modificacao=None, 
                    vEh_Assinado=False, vEh_Versao_Atual= True):
        try:
            iDocumento  = Documento.objects.filter(id_documento= vIDDocumento)[0]
            iCriador    = Usuario.objects.filter(id= vIDCriador)[0]
            iEstado     = Estado_da_Versao.objects.filter(id_estado_da_versao= vIDEstado)[0]
            iUpload     = MultiuploaderImage.objects.filter(key_data = vUploadKeyData)[0]

            iVersao                 = Versao()
            iVersao.documento       = iDocumento
            iVersao.usr_criador     = iCriador
            iVersao.estado          = iEstado
            iVersao.versao          = vVersao
            iVersao.dsc_modificacao = vDsc_Modificacao
            iVersao.upload          = iUpload
            iVersao.protocolo       = vProtocolo
            iVersao.data_criacao    = str(datetime.datetime.today())[:19]
            iVersao.eh_assinado     = vEh_Assinado
            iVersao.eh_versao_atual = vEh_Versao_Atual
            iVersao.save()
            return iVersao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar a Versao do Documento: ' + str(e))
            return False
        
    def buscaDocumentos(self, vIDEmpresa, vAssunto= None, vProtocolo= None, vIDUsuarioResponsavel= None, vIDUsuarioCriador= None, 
                        vIDTipoDocumento= None, vIDEstadoDoDocumento= None, vDataDeCriacaoInicial= None, 
                        vDataDeCriacaoFinal= None, vListaIndice= None, vEhPublico= False):
        try:
            if vEhPublico:
                iListaDeVersoesEncontradas= Versao.objects.filter(eh_versao_atual= True, documento__empresa__id_empresa= vIDEmpresa, 
                                                                  documento__eh_publico= True)
            else:
                iListaDeVersoesEncontradas= Versao.objects.filter(eh_versao_atual= True, documento__empresa__id_empresa= vIDEmpresa)
            if vAssunto not in (None, ''):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(documento__assunto__icontains= vAssunto)
            if vProtocolo not in (None, ''):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(protocolo__exact= vProtocolo)
            if vIDUsuarioResponsavel not in (None, '', 'selected'):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(documento__usr_responsavel__id= int(vIDUsuarioResponsavel))
            if vIDUsuarioCriador not in (None, '', 'selected'):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(usr_criador__id= int(vIDUsuarioCriador))
            if vIDTipoDocumento not in (None, '', 'selected'):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(documento__tipo_documento__id_tipo_documento= int(vIDTipoDocumento))
            if vIDEstadoDoDocumento not in (None, '', 'selected'):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(estado__id_estado_da_versao= int(vIDEstadoDoDocumento))
            if vDataDeCriacaoInicial not in (None, ''):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(data_criacao__gt= vDataDeCriacaoInicial)
            if vDataDeCriacaoFinal not in (None, ''):
                iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(data_criacao__lt= vDataDeCriacaoFinal)
            if vListaIndice not in (None, ''):
                iListaVersoesIndice= []
                mIndice_Versao_Valor= get_model('indice', 'Indice_Versao_Valor')
                for x in range(len(vListaIndice)):
                    iIDIndice, iValorIndice= vListaIndice[x]
                    for i in range(len(iListaDeVersoesEncontradas)):
                        iListaVersoesIndice= mIndice_Versao_Valor().obtemIDVersoesFiltradosPorIndice(vIDEmpresa, iIDIndice, iValorIndice)
                        iListaDeVersoesEncontradas= iListaDeVersoesEncontradas.filter(id_versao__in = iListaVersoesIndice)
            iListaDocumentosAuxiliar= []
            for i in range(len(iListaDeVersoesEncontradas)):
                iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(iListaDeVersoesEncontradas[i].documento)
                iDocumentoAuxiliar= Versao().obtemDocumentoAuxiliar(iVersaoAtual)
                iListaDocumentosAuxiliar.append(iDocumentoAuxiliar)
            return iListaDocumentosAuxiliar
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel buscar os Documentos: ' + str(e))
            return False 
        
