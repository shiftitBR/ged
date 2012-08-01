'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models

from autenticacao.models        import Empresa #@UnresolvedImport
from autenticacao.models        import Usuario #@UnresolvedImport
from documento.models           import Versao #@UnresolvedImport
from objetos_auxiliares         import Documento as DocumentoAuxiliar
from objetos_auxiliares         import Historico as HistoricoAuxiliar

import datetime
import logging
import constantes #@UnresolvedImport

#-----------------------------HISTORICO----------------------------------------

class Tipo_de_Evento(models.Model):
    id_tipo_evento          = models.IntegerField(max_length=3, primary_key=True)
    descricao               = models.CharField(max_length=30)

    class Meta:
        db_table= 'tb_tipo_de_evento'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Tipo_de_Evento.objects.order_by('-id_tipo_evento')) > 0:   
            iUltimoRegistro = Tipo_de_Evento.objects.order_by('-id_tipo_evento')[0] 
            self.id_tipo_evento= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_evento= 1
        super(Tipo_de_Evento, self).save()

class Historico(models.Model):
    id_historico    = models.IntegerField(max_length=10, primary_key=True, blank=True)
    versao          = models.ForeignKey(Versao, null= False)
    tipo_evento     = models.ForeignKey(Tipo_de_Evento, null= False)
    usuario         = models.ForeignKey(Usuario, null= False)
    data            = models.CharField(max_length=100, null= False)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_historico'
    
    def __unicode__(self):
        return str(self.id_historico)
    
    def save(self): 
        if self.id_historico == '' or self.id_historico== None:
            if len(Historico.objects.order_by('-id_historico')) > 0:   
                iUltimoRegistro = Historico.objects.order_by('-id_historico')[0] 
                self.id_historico= iUltimoRegistro.pk + 1
            else:
                self.id_historico= 1
        super(Historico, self).save()  
    
    def salvaHistorico(self, vIDVersao, vIDTipo_Evento, vIDUsuario, vIDEmpresa, 
                       vData= str(datetime.datetime.today())[:19]):
        try:
            iVersao         = Versao.objects.filter(id_versao= vIDVersao)[0]
            iTipoEvento     = Tipo_de_Evento.objects.filter(id_tipo_evento= vIDTipo_Evento)[0]
            iUsuario        = Usuario.objects.filter(id= vIDUsuario)[0]
            iEmpresa        = Empresa.objects.filter(id_empresa= vIDEmpresa)[0]
            
            iHistorico              = Historico()
            iHistorico.versao       = iVersao
            iHistorico.tipo_evento  = iTipoEvento
            iHistorico.usuario      = iUsuario
            iHistorico.empresa      = iEmpresa
            iHistorico.data         = vData
            iHistorico.save()
            return iHistorico
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar o Historico: ' + str(e))
            return False 
        
    def obtemListaEventos(self, vIDVersao):
        try: 
            iVersaoDoc      = Versao.objects.filter(id_versao= vIDVersao)[0]
            iListaHistorico = Historico.objects.filter(versao__documento= iVersaoDoc.documento).order_by('versao')
            iLista      = []
            for i in range(len(iListaHistorico)):
                iHistorico= iListaHistorico[i]
                iCriador= iHistorico.usuario
                iNomeUsuario= iCriador.first_name + ' ' + iCriador.last_name 
                iHistoricoAux= HistoricoAuxiliar()
                iHistoricoAux.idHistorico       = iHistorico.id_historico
                iHistoricoAux.dataEvento        = iHistorico.data
                iHistoricoAux.dscEvento         = iHistorico.tipo_evento.descricao
                iHistoricoAux.idTipoEvento      = iHistorico.tipo_evento.id_tipo_evento
                iHistoricoAux.num_versao        = iHistorico.versao.versao
                iHistoricoAux.dsc_modificacao   = iHistorico.versao.dsc_modificacao
                iHistoricoAux.nomeUsuario       = iNomeUsuario
                iLista.append(iHistoricoAux)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaVersao: ' + str(e))
            return False 
    
    def calculaQuantidadeDeVisualizacoesDoDocumento(self, vVersao):
        try:
            iVisualizacoes= len(Historico.objects.filter(versao__documento= vVersao.documento.id_documento).filter(
                                                                    tipo_evento= constantes.cntEventoHistoricoVisualizar))
            return iVisualizacoes
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel calculaQuantidadeDeVisualizacoesDoDocumento: ' + str(e))
            return False 
        
    def calculaQuantidadeDeDownloadsDoDocumento(self, vVersao):
        try:
            iDownloads= len(Historico.objects.filter(versao__documento= vVersao.documento.id_documento).filter(
                                                                    tipo_evento= constantes.cntEventoHistoricoDownload))
            return iDownloads
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel calculaQuantidadeDeDownloadsDoDocumento: ' + str(e))
            return False 