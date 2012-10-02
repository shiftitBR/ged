# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from autenticacao.models                import Usuario #@UnresolvedImport
from documento.models                   import Versao #@UnresolvedImport
from objetos_auxiliares                 import Pendencia as PendenciaAuxiliar

from PyProject_GED.autenticacao.models  import Empresa
from PyProject_GED.documento.models     import Tipo_de_Documento
from PyProject_GED.seguranca.models     import Pasta, Grupo, Grupo_Usuario
from PyProject_GED.historico.models     import Historico
from PyProject_GED                      import constantes
from PyProject_GED.documento.controle   import Controle as DocumentoControle

import logging
import datetime


#-----------------------------Workflow----------------------------------------

class Tipo_de_Pendencia(models.Model):
    id_tipo_de_pendencia   = models.IntegerField(max_length=3, primary_key=True)
    descricao       = models.CharField(max_length=200, null= False)
    
    class Meta:
        db_table= 'tb_tipo_de_pendencia'
        verbose_name = 'Tipo de Pendência'
        verbose_name_plural = 'Tipos de Pendência'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if self.id_tipo_de_pendencia == '' or self.id_tipo_de_pendencia== None:
            if len(Tipo_de_Pendencia.objects.order_by('-id_tipo_de_pendencia')) > 0:   
                iUltimoRegistro = Tipo_de_Pendencia.objects.order_by('-id_tipo_de_pendencia')[0] 
                self.id_tipo_de_pendencia= iUltimoRegistro.pk + 1
            else:
                self.id_tipo_de_pendencia= 1
        super(Tipo_de_Pendencia, self).save()

class Workflow(models.Model):
    id_workflow         = models.IntegerField(max_length=5, primary_key=True)
    empresa             = models.ForeignKey(Empresa, unique=False)
    tipo_de_documento   = models.ForeignKey(Tipo_de_Documento, null= False)
    pasta               = models.ForeignKey(Pasta, null= False)
    descricao           = models.CharField(max_length=200, null= False)
    
    class Meta:
        db_table= 'tb_workflow'
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflow'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if self.id_workflow == '' or self.id_workflow== None:
            if len(Workflow.objects.order_by('-id_workflow')) > 0:   
                iUltimoRegistro = Workflow.objects.order_by('-id_workflow')[0] 
                self.id_workflow= iUltimoRegistro.pk + 1
            else:
                self.id_workflow= 1
        super(Workflow, self).save()
    
    def obtemWorkflow(self, vPasta, vTipoDoDocumento):
        try:
            iListaWorkflow= Workflow.objects.filter(tipo_de_documento= vTipoDoDocumento, pasta= vPasta)
            if len(iListaWorkflow) > 0:
                iWorkflow= iListaWorkflow[0]
            else:
                iWorkflow= None
            return iWorkflow
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter Workflow: ' + str(e))
            return False
    
    def obtemEtapaAtual(self, vWorkflow, vVersao):
        try:
            iListaPendenciasDoWorkflow= Pendencia.objects.filter(workflow= vWorkflow, versao=vVersao)
            iOrdemEtapaAtual= -1
            iListaEtapaAtual= Etapa_do_Workflow.objects.filter(workflow= vWorkflow, ordem_da_etapa= 0)
            if len(iListaEtapaAtual) > 0: 
                iEtapaAtual= iListaEtapaAtual[0]
            else:
                iEtapaAtual= None
            for iPendencia in iListaPendenciasDoWorkflow:
                if iOrdemEtapaAtual < iPendencia.etapa_do_workflow.ordem_da_etapa:
                    iEtapaAtual= iPendencia.etapa_do_workflow
                    iOrdemEtapaAtual= iEtapaAtual.ordem_da_etapa
            return iEtapaAtual
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a Etapa Atual: ' + str(e))
            return False
    
    def obtemProximaEtapa(self, vWorkflow, vVersaoAtual):
        try:
            iListaEtapas= Etapa_do_Workflow.objects.filter(workflow= vWorkflow).order_by('ordem_da_etapa')
            if len(iListaEtapas) == 0:
                return None
            iOrdemEtapaAtual= self.obtemEtapaAtual(vWorkflow, vVersaoAtual).ordem_da_etapa
            iProximaEtapa= None
            if iOrdemEtapaAtual < len(iListaEtapas) -1:
                iOrdemProximaEtapa= iOrdemEtapaAtual + 1
                iProximaEtapa= iListaEtapas[iOrdemProximaEtapa]
            return iProximaEtapa
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a Proxima Etapa: ' + str(e))
            return False
    
    def verificaSeEtapaAtualEstaConcluida(self, vWorkflow, vDocumento):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iEtapaAtual= self.obtemEtapaAtual(vWorkflow, iVersaoAtual)
            if iEtapaAtual in (None, False):
                return None
            iListaPendenciasDaEtapa= Pendencia.objects.filter(workflow= vWorkflow, etapa_do_workflow= iEtapaAtual, versao= iVersaoAtual)
            iPendenciasConcluidas= 0
            for iPendencia in iListaPendenciasDaEtapa:
                if iPendencia.estado_da_pendencia.id_estado_da_pendencia == constantes.cntEstadoPendenciaConcluida: 
                    iPendenciasConcluidas= iPendenciasConcluidas + 1
            if (iEtapaAtual.eh_multipla) and (iPendenciasConcluidas == len(iListaPendenciasDaEtapa)):
                iConcluido= True
            elif not iEtapaAtual.eh_multipla and (iPendenciasConcluidas > 0):
                iConcluido= True
            else:
                iConcluido= False
            return iConcluido
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel verificar se etapa atual esta concluida: ' + str(e))
            return False
    
    def executaWorkflow(self, vDocumento, vAcao=None, vUsuario=None):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iPasta= vDocumento.pasta
            iTipoDoDocumento= vDocumento.tipo_documento
            iWorkflow= self.obtemWorkflow(iPasta, iTipoDoDocumento)
            iEtapaAtualConcluida= self.verificaSeEtapaAtualEstaConcluida(iWorkflow, vDocumento)
            if (iWorkflow not in (None, False)) and (iEtapaAtualConcluida not in (None, False)):
                Pendencia().cancelaPendenciasDoWorkflow(iWorkflow, vDocumento)
                iEtapaAtual= self.obtemEtapaAtual(iWorkflow, iVersaoAtual)
                iProximaEtapa= self.obtemProximaEtapa(iWorkflow, iVersaoAtual)
                if iProximaEtapa not in (None, False):
                    Pendencia().criaPendenciasDoWorkflow(vDocumento, iProximaEtapa)
                elif (iProximaEtapa == None):
                    Pendencia().alteraEstadoDoDocumento(iEtapaAtual.tipo_de_pendencia, vDocumento, vAcao, vUsuario)
            elif (iWorkflow == None) or (iEtapaAtualConcluida == None):
                return None  
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel executar o Workflow: ' + str(e))
            return False
    
class Etapa_do_Workflow(models.Model):
    id_etapa_do_workflow    = models.IntegerField(max_length=5, primary_key=True)
    ordem_da_etapa          = models.IntegerField(max_length=3, null= False)
    workflow                = models.ForeignKey(Workflow, null= False)
    grupo                   = models.ForeignKey(Grupo, null= False)
    tipo_de_pendencia       = models.ForeignKey(Tipo_de_Pendencia, null= False)
    eh_multipla             = models.BooleanField(null= False, verbose_name='Multiplo', help_text='Indica que todos os usuários de determinado grupo devem efetuar a ação desejada.')
    descricao               = models.CharField(max_length=200, null= False)
    
    class Meta:
        db_table= 'tb_etapa_do_workflow'
        verbose_name = 'Etapa do Workflow'
        verbose_name_plural = 'Etapas do Workflow'
    
    def __unicode__(self):
        return str(self.id_etapa_do_workflow)
    
    def save(self): 
        try: 
            if self.id_etapa_do_workflow == '' or self.id_etapa_do_workflow== None:
                if len(Etapa_do_Workflow.objects.order_by('-id_etapa_do_workflow')) > 0:   
                    iUltimoRegistro = Etapa_do_Workflow.objects.order_by('-id_etapa_do_workflow')[0] 
                    self.id_etapa_do_workflow= iUltimoRegistro.pk + 1
                else:
                    self.id_etapa_do_workflow= 1
                
                iListaEtapas= Etapa_do_Workflow.objects.filter(workflow= self.workflow).order_by('-ordem_da_etapa')
                if len(iListaEtapas) == 0:
                    self.ordem_da_etapa= 0
                else:
                    self.ordem_da_etapa= iListaEtapas[len(iListaEtapas)-1].ordem_da_etapa + 1
                
            super(Etapa_do_Workflow, self).save()
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar a Etapa do Workflow: ' + str(e))
            return False
        

#-----------------------------Pendencia----------------------------------------
        
class Grupo_da_Pendencia(models.Model):
    id_grupo_da_pendencia   = models.IntegerField(max_length=5, primary_key=True)
    eh_multipla             = models.BooleanField(null= False, verbose_name='Multiplo')
    
    class Meta:
        db_table= 'tb_grupo_da_pendencia'
        verbose_name = 'Grupo da Pendência'
        verbose_name_plural = 'Grupos da Pendência'
    
    def __unicode__(self):
        return str(self.id_estado_da_pendencia)
    
    def save(self):  
        if len(Grupo_da_Pendencia.objects.order_by('-id_grupo_da_pendencia')) > 0:   
            iUltimoRegistro = Grupo_da_Pendencia.objects.order_by('-id_grupo_da_pendencia')[0] 
            self.id_grupo_da_pendencia= iUltimoRegistro.pk + 1
        else:
            self.id_grupo_da_pendencia= 1
        super(Grupo_da_Pendencia, self).save()
        
    def criaGrupoDaPendencia(self, vEhMultipla):
        try:
            iGrupoDaPendencia= Grupo_da_Pendencia(vEhMultipla)
            iGrupoDaPendencia.save()
            return iGrupoDaPendencia
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Grupo da Pendencia: ' + str(e))
            return False


class Estado_da_Pendencia(models.Model):
    id_estado_da_pendencia  = models.IntegerField(max_length=3, primary_key=True)
    descricao               = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_estado_da_pendencia'
        verbose_name = 'Estado da Pendência'
        verbose_name_plural = 'Estados da Pendência'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Estado_da_Pendencia.objects.order_by('-id_estado_da_pendencia')) > 0:   
            iUltimoRegistro = Estado_da_Pendencia.objects.order_by('-id_estado_da_pendencia')[0] 
            self.id_estado_da_pendencia= iUltimoRegistro.pk + 1
        else:
            self.id_estado_da_pendencia= 1
        super(Estado_da_Pendencia, self).save()

class Pendencia(models.Model):
    id_pendencia        = models.IntegerField(max_length=3, primary_key=True)
    estado_da_pendencia = models.ForeignKey(Estado_da_Pendencia, null= False)
    usr_remetente       = models.ForeignKey(Usuario, blank=True, unique=False, verbose_name='user', related_name="usr_remetente")
    usr_destinatario    = models.ForeignKey(Usuario, blank=True, unique=False, verbose_name='user', related_name="usr_destinatario")
    versao              = models.ForeignKey(Versao, null= False)
    tipo_de_pendencia   = models.ForeignKey(Tipo_de_Pendencia, null= False)
    workflow            = models.ForeignKey(Workflow, null= True)
    etapa_do_workflow   = models.ForeignKey(Etapa_do_Workflow, null= True)
    grupo_da_pendencia  = models.ForeignKey(Grupo_da_Pendencia, null= True)
    data                = models.DateTimeField(null= False)
    descricao           = models.CharField(max_length=200, null= False)
    feedback            = models.CharField(max_length=200, null= True)
    
    class Meta:
        db_table= 'tb_pendencia'
        verbose_name = 'Pendência'
        verbose_name_plural = 'Pendências'
    
    def __unicode__(self):
        return str(self.id_pendencia)
    
    def save(self): 
        if self.id_pendencia == '' or self.id_pendencia== None:
            if len(Pendencia.objects.order_by('-id_pendencia')) > 0:   
                iUltimoRegistro = Pendencia.objects.order_by('-id_pendencia')[0] 
                self.id_pendencia= iUltimoRegistro.pk + 1
            else:
                self.id_pendencia= 1
            self.estado_da_pendencia= Estado_da_Pendencia.objects.filter(id_estado_da_pendencia= constantes.cntEstadoPendenciaPendente)[0]
        super(Pendencia, self).save()
        
    def criaPendencia(self, vRemetente, vListaDestinatarios, vVersao, vDescricao, vTipoDePendencia, 
                      vWorkflow=None, vEtapaDoWorkflow=None, vEhMultipla= False):
        try:
            iGrupo_da_Pendencia= None
            if len(vListaDestinatarios) > 1:
                iGrupo_da_Pendencia= Grupo_da_Pendencia().criaGrupoDaPendencia(vEhMultipla)
            for iDestinatario in vListaDestinatarios:
                iPendencia= Pendencia()
                iPendencia.usr_remetente        = vRemetente
                iPendencia.usr_destinatario     = iDestinatario
                iPendencia.versao               = vVersao   
                iPendencia.data                 = str(datetime.datetime.today())[:19]    
                iPendencia.descricao            = vDescricao
                iPendencia.tipo_de_pendencia    = vTipoDePendencia
                iPendencia.workflow             = vWorkflow
                iPendencia.grupo_da_pendencia   = iGrupo_da_Pendencia
                iPendencia.etapa_do_workflow    = vEtapaDoWorkflow
                iPendencia.save()
            
            Versao().alterarEstadoVersao(vVersao.id_versao, constantes.cntEstadoVersaoPendente)
            Historico().salvaHistorico(vVersao.id_versao, constantes.cntEventoHistoricoEncaminhar, 
                                       vRemetente.id, vVersao.documento.empresa.id_empresa)
            
            return iPendencia
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a pendencia: ' + str(e))
            return False
    
    def criaPendenciasDoWorkflow(self, vDocumento, vProximaEtapa=None):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iPasta= vDocumento.pasta
            iTipoDoDocumento= vDocumento.tipo_documento
            iWorkflow= Workflow().obtemWorkflow(iPasta, iTipoDoDocumento)           
            if vProximaEtapa != None:
                iEtapa= vProximaEtapa
            else:
                iEtapa= Workflow().obtemEtapaAtual(iWorkflow, iVersaoAtual)
            if iEtapa == None:
                return None
            iGrupo= iEtapa.grupo
            iListaGrupoUsuarios= Grupo_Usuario.objects.filter(grupo= iGrupo)
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            for iGrupoUsuario in iListaGrupoUsuarios:
                iListaDestinatarios= []
                iListaDestinatarios.append(iGrupoUsuario.usuario)
                self.criaPendencia(iVersaoAtual.usr_criador, iListaDestinatarios, iVersaoAtual, 
                                        iEtapa.descricao, iEtapa.tipo_de_pendencia, 
                                        iWorkflow, iEtapa)
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a pendencia do workflow: ' + str(e))
            return False
        
    def obtemPendencia(self, vVersao, vDestinatario):
        try:
            iPendencia= Pendencia.objects.filter(versao=vVersao.id_versao).filter(usr_destinatario=vDestinatario.id)[0]
            return iPendencia
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem Pendencia: ' + str(e))
            return False
    
    def cancelaPendenciasDoWorkflow(self, vWorkflow, vDocumento):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iEtapaAtual= Workflow().obtemEtapaAtual(vWorkflow, iVersaoAtual)
            iListaPendenciasDaEtapa= Pendencia.objects.filter(workflow= vWorkflow, etapa_do_workflow= iEtapaAtual, 
                                                              estado_da_pendencia= constantes.cntEstadoPendenciaPendente,
                                                              versao= iVersaoAtual)
            for iPendencia in iListaPendenciasDaEtapa:
                self.cancelaPendencia(iPendencia)
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel cancelar as pendencias do workflow: ' + str(e))
            return False
    
    def cancelaPendenciasDoGrupo(self, vGrupoDaPendencia, vDocumento):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iListaPendenciasDaGrupo= Pendencia.objects.filter(grupo_da_pendencia= vGrupoDaPendencia, 
                                                              estado_da_pendencia= constantes.cntEstadoPendenciaPendente,
                                                              versao= iVersaoAtual)
            for iPendencia in iListaPendenciasDaGrupo:
                self.cancelaPendencia(iPendencia)
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel cancelar as pendencias do grupo: ' + str(e))
            return False
        
    def obtemListaPendenciasRemetente(self, vRemetente):
        try:
            iListaPendencias = Pendencia.objects.filter(usr_remetente= vRemetente).order_by('-data')
            iNomeRemetente   = Usuario().obterNomeUsuario(vRemetente.id)
            iLista= []
            for i in range(len(iListaPendencias)):
                iNomeDestinatario = Usuario().obterNomeUsuario(iListaPendencias[i].usr_destinatario.id)
                iPendencia= PendenciaAuxiliar()
                iPendencia.data         = DocumentoControle().formataData(iListaPendencias[i].data)
                iPendencia.descricao    = iListaPendencias[i].descricao
                iPendencia.destinatario = iNomeDestinatario
                iPendencia.estadoDoc    = iListaPendencias[i].versao.estado.descricao
                if iListaPendencias[i].feedback == None:
                    iFeedback= '-- --'
                else:
                    iFeedback= iListaPendencias[i].feedback
                iPendencia.feedback     = iFeedback
                iPendencia.idPendencia  = iListaPendencias[i].id_pendencia
                iPendencia.idVersao     = iListaPendencias[i].versao.id_versao
                iPendencia.protocolo    = iListaPendencias[i].versao.protocolo
                iPendencia.remetente    = iNomeRemetente
                iPendencia.idEstadoDoc  = iListaPendencias[i].versao.estado.id_estado_da_versao
                iPendencia.idEstadoPen  = iListaPendencias[i].estado_da_pendencia.id_estado_da_pendencia
                iPendencia.estadoPen    = iListaPendencias[i].estado_da_pendencia.descricao
                iLista.append(iPendencia)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaPendenciasRemetente: ' + str(e))
            return False
        
    def obtemListaPendenciasDestinatario(self, vDestinatario):
        try:
            iListaPendencias = Pendencia.objects.filter(usr_destinatario= vDestinatario).filter(
                                                estado_da_pendencia= constantes.cntEstadoPendenciaPendente).order_by('-data')
            iNomeDestinatario= Usuario().obterNomeUsuario(vDestinatario.id)
            iLista= []
            for i in range(len(iListaPendencias)):
                iNomeRemetente = Usuario().obterNomeUsuario(iListaPendencias[i].usr_remetente.id)
                iPendencia= PendenciaAuxiliar()
                iPendencia.data         = DocumentoControle().formataData(iListaPendencias[i].data)
                iPendencia.descricao    = iListaPendencias[i].descricao
                iPendencia.destinatario = iNomeDestinatario
                iPendencia.estadoDoc    = iListaPendencias[i].versao.estado.descricao
                iPendencia.tipo         = iListaPendencias[i].tipo_de_pendencia.id_tipo_de_pendencia
                if iListaPendencias[i].feedback == None:
                    iFeedback= '-- --'
                else:
                    iFeedback= iListaPendencias[i].feedback
                iPendencia.feedback     = iFeedback
                iPendencia.idPendencia  = iListaPendencias[i].id_pendencia
                iPendencia.idVersao     = iListaPendencias[i].versao.id_versao
                iPendencia.protocolo    = iListaPendencias[i].versao.protocolo
                iPendencia.remetente    = iNomeRemetente
                iPendencia.idEstadoDoc  = iListaPendencias[i].versao.estado.id_estado_da_versao
                iPendencia.idEstadoPen  = iListaPendencias[i].estado_da_pendencia.id_estado_da_pendencia
                iPendencia.estadoPen    = iListaPendencias[i].estado_da_pendencia.descricao
                iLista.append(iPendencia)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaPendenciasDestinatario: ' + str(e))
            return False
    
    def obtemQuantidadePendenciasDestinatario(self, vDestinatarioID):
        try:
            iQuantiadePendencias = Pendencia.objects.filter(usr_destinatario__id= vDestinatarioID).filter(
                                                estado_da_pendencia= constantes.cntEstadoPendenciaPendente).count()
            return iQuantiadePendencias
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaPendenciasDestinatario: ' + str(e))
            return False
        
    def adicionarFeedback(self, vComentario, vPendencia):
        try:
            vPendencia.feedback= vComentario
            vPendencia.save()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel adicionarFeedback: ' + str(e))
            return False
    
    def concluiPendencia(self, vPendencia, vComentario=None):
        try:
            if vPendencia.estado_da_pendencia.id_estado_da_pendencia == constantes.cntEstadoPendenciaPendente :
                iNovoEstado= Estado_da_Pendencia.objects.filter(id_estado_da_pendencia= constantes.cntEstadoPendenciaConcluida)[0]
                vPendencia.estado_da_pendencia= iNovoEstado
                if vComentario != None:
                    self.adicionarFeedback(vComentario, vPendencia)
            vPendencia.save()
            return vPendencia
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel concluir pendencia: ' + str(e))
            return False   
    
    def cancelaPendencia(self, vPendencia):
        try:
            if vPendencia.estado_da_pendencia.id_estado_da_pendencia == constantes.cntEstadoPendenciaPendente:
                iNovoEstado= Estado_da_Pendencia.objects.filter(id_estado_da_pendencia= constantes.cntEstadoPendenciaCancelada)[0]
                vPendencia.estado_da_pendencia= iNovoEstado
            Historico().salvaHistorico(vPendencia.versao.id_versao, constantes.cntEventoHistoricoCancelarPendencia, 
                                   vPendencia.usr_remetente.id, vPendencia.versao.documento.empresa.id_empresa)
            vPendencia.save()
            return vPendencia
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel cancelar pendencia: ' + str(e))
            return False
    
    def verificaSeGrupoAtualEstaConcluido(self, vGrupoDaPendencia, vDocumento):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iListaPendenciasDoGrupo= Pendencia.objects.filter(grupo_da_pendencia= vGrupoDaPendencia, versao= iVersaoAtual)
            iPendenciasConcluidas= 0
            for iPendencia in iListaPendenciasDoGrupo:
                if iPendencia.estado_da_pendencia.id_estado_da_pendencia == constantes.cntEstadoPendenciaConcluida: 
                    iPendenciasConcluidas= iPendenciasConcluidas + 1
            if (vGrupoDaPendencia.eh_multipla) and (iPendenciasConcluidas == len(iListaPendenciasDoGrupo)):
                iConcluido= True
            elif not vGrupoDaPendencia.eh_multipla and (iPendenciasConcluidas > 0):
                iConcluido= True
            else:
                iConcluido= False
            return iConcluido
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel verificar se grupo atual esta concluido: ' + str(e))
            return False
    
    def alteraEstadoDoDocumento(self, vTipoDePendencia, vDocumento, vAcao, vUsuario):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            if vTipoDePendencia.id_tipo_de_pendencia == constantes.cntTipoPendenciaAprovacao:
                if vAcao == constantes.cntAcaoPendenciaAprovar:
                    Versao().alterarEstadoVersao(iVersaoAtual.id_versao, constantes.cntEstadoVersaoAprovado)
                    Historico().salvaHistorico(iVersaoAtual.id_versao, constantes.cntEventoHistoricoAprovar, 
                                   vUsuario.id, vDocumento.empresa.id_empresa)
                else:
                    Versao().alterarEstadoVersao(iVersaoAtual.id_versao, constantes.cntEstadoVersaoReprovado)
                    Historico().salvaHistorico(iVersaoAtual.id_versao, constantes.cntEventoHistoricoReprovar, 
                                   vUsuario.id, vDocumento.empresa.id_empresa)
            elif vTipoDePendencia.id_tipo_de_pendencia == constantes.cntTipoPendenciaAssintaura:
                Versao().alterarEstadoVersao(iVersaoAtual.id_versao, constantes.cntEstadoVersaoDisponivel) 
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel alterar estado do Documento da Pendencia: ' + str(e))
            return False
    
    def trataPendencia(self, vDocumento, vAcao, vUsuario, vComentario=None):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iPendencia= Pendencia.objects.filter(versao= iVersaoAtual, usr_destinatario= vUsuario,
                                                 estado_da_pendencia= constantes.cntEstadoPendenciaPendente)[0]
            self.concluiPendencia(iPendencia, vComentario)
            iGrupoDaPendencia= iPendencia.grupo_da_pendencia
            iWorkflow= iPendencia.workflow
            if (iGrupoDaPendencia not in (None, False)) and (self.verificaSeGrupoAtualEstaConcluido(iGrupoDaPendencia, vDocumento) or vAcao == constantes.cntAcaoPendenciaReprovar):
                self.cancelaPendenciasDoGrupo(iGrupoDaPendencia, vDocumento)
                self.alteraEstadoDoDocumento(iPendencia.tipo_de_pendencia, vDocumento, vAcao, vUsuario)
            elif iWorkflow not in (None, False):
                if vAcao == constantes.cntAcaoPendenciaReprovar:
                    self.cancelaPendenciasDoWorkflow(iWorkflow, vDocumento)
                    self.alteraEstadoDoDocumento(iPendencia.tipo_de_pendencia, vDocumento, vAcao, vUsuario)
                elif Workflow().verificaSeEtapaAtualEstaConcluida(iWorkflow, vDocumento):
                    Workflow().executaWorkflow(vDocumento, vAcao, vUsuario)
            elif iGrupoDaPendencia == None and iWorkflow == None:
                self.alteraEstadoDoDocumento(iPendencia.tipo_de_pendencia, vDocumento, vAcao, vUsuario)
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel tratar a pendencia: ' + str(e))
            return False

    def obtemListaDeDestinatariosPendentes(self, vDocumento):
        try:
            iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(vDocumento)
            iListaPendencias= Pendencia.objects.filter(versao= iVersaoAtual, estado_da_pendencia= constantes.cntEstadoPendenciaPendente)
            iListaDestinatarios= []
            for iPendencia in iListaPendencias:
                iListaDestinatarios.append(iPendencia.usr_destinatario)
            iListaDestinatariosUnicos= list(set(iListaDestinatarios))
            return iListaDestinatariosUnicos
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter lista de destinatarios pendentes: ' + str(e))
            return False