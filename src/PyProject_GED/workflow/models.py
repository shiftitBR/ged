# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from autenticacao.models                import Usuario #@UnresolvedImport
from documento.models                   import Versao #@UnresolvedImport
from objetos_auxiliares                 import Pendencia as PendenciaAuxiliar

import logging
import datetime
import constantes #@UnresolvedImport
from PyProject_GED.autenticacao.models import Empresa
from PyProject_GED.documento.models import Tipo_de_Documento
from PyProject_GED.seguranca.models import Pasta, Grupo

#-----------------------------Pendencia----------------------------------------

class Tipo_de_Pendencia(models.Model):
    id_tipo_de_pendencia   = models.IntegerField(max_length=3, primary_key=True)
    descricao       = models.CharField(max_length=200, null= False)
    
    class Meta:
        db_table= 'tb_tipo_de_pendencia'
        verbose_name = 'Tipo de Pendência'
        verbose_name_plural = 'Tipos de Pendência'
    
    def __unicode__(self):
        return str(self.id_tipo_de_pendencia)

class Pendencia(models.Model):
    id_pendencia    = models.IntegerField(max_length=3, primary_key=True)
    usr_remetente   = models.ForeignKey(Usuario, blank=True, unique=False, verbose_name='user', related_name="usr_remetente")
    usr_destinatario= models.ForeignKey(Usuario, blank=True, unique=False, verbose_name='user', related_name="usr_destinatario")
    versao          = models.ForeignKey(Versao, null= False)
    data            = models.CharField(max_length=100, null= False)
    descricao       = models.CharField(max_length=200, null= False)
    feedback        = models.CharField(max_length=200, null= True)
    
    class Meta:
        db_table= 'tb_pendencia'
        verbose_name = 'Pendência'
        verbose_name_plural = 'Pendências'
    
    def __unicode__(self):
        return self.id_pendencia
    
    def save(self):  
        if self.id_pendencia == '' or self.id_pendencia== None:
            if len(Pendencia.objects.order_by('-id_pendencia')) > 0:   
                iUltimoRegistro = Pendencia.objects.order_by('-id_pendencia')[0] 
                self.id_pendencia= iUltimoRegistro.pk + 1
            else:
                self.id_pendencia= 1
        super(Pendencia, self).save()
        
    def criaPendencia(self, vRemetente, vDestinatario, vVersao, vDescricao, vData=str(datetime.datetime.today())[:19]):
        try:
            iPendencia= Pendencia()
            iPendencia.usr_remetente    = vRemetente
            iPendencia.usr_destinatario = vDestinatario
            iPendencia.versao           = vVersao   
            iPendencia.data             = vData    
            iPendencia.descricao        = vDescricao
            iPendencia.save()
            return iPendencia
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a pendencia: ' + str(e))
            return False
        
    def obtemListaPendenciasRemetente(self, vRemetente):
        try:
            iListaPendencias = Pendencia.objects.filter(usr_remetente= vRemetente).order_by('data')
            iNomeRemetente   = vRemetente.first_name + ' ' + vRemetente.last_name
            iLista= []
            for i in range(len(iListaPendencias)):
                iNomeDestinatario = iListaPendencias[i].usr_destinatario.first_name + ' ' + iListaPendencias[i].usr_destinatario.last_name
                iPendencia= PendenciaAuxiliar()
                iPendencia.data         = iListaPendencias[i].data
                iPendencia.descricao    = iListaPendencias[i].descricao
                iPendencia.destinatario = iNomeDestinatario
                iPendencia.estado       = iListaPendencias[i].versao.estado.descricao
                if iListaPendencias[i].feedback == None:
                    iFeedback= '-- --'
                else:
                    iFeedback= iListaPendencias[i].feedback
                iPendencia.feedback     = iFeedback
                iPendencia.idPendencia  = iListaPendencias[i].id_pendencia
                iPendencia.idVersao     = iListaPendencias[i].versao.id_versao
                iPendencia.protocolo    = iListaPendencias[i].versao.protocolo
                iPendencia.remetente    = iNomeRemetente
                iLista.append(iPendencia)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaPendenciasRemetente: ' + str(e))
            return False
        
    def obtemListaPendenciasDestinatario(self, vDestinatario):
        try:
            iListaPendencias = Pendencia.objects.filter(usr_destinatario= vDestinatario).filter(
                                                versao__estado__id_estado_da_versao= constantes.cntEstadoVersaoPendente).order_by('data')
            iNomeDestinatario= vDestinatario.first_name + ' ' + vDestinatario.last_name
            iLista= []
            for i in range(len(iListaPendencias)):
                iNomeRemetente = iListaPendencias[i].usr_remetente.first_name + ' ' + iListaPendencias[i].usr_remetente.last_name
                iPendencia= PendenciaAuxiliar()
                iPendencia.data         = iListaPendencias[i].data
                iPendencia.descricao    = iListaPendencias[i].descricao
                iPendencia.destinatario = iNomeDestinatario
                iPendencia.estado       = iListaPendencias[i].versao.estado.descricao
                if iListaPendencias[i].feedback == None:
                    iFeedback= '-- --'
                else:
                    iFeedback= iListaPendencias[i].feedback
                iPendencia.feedback     = iFeedback
                iPendencia.idPendencia  = iListaPendencias[i].id_pendencia
                iPendencia.idVersao     = iListaPendencias[i].versao.id_versao
                iPendencia.protocolo    = iListaPendencias[i].versao.protocolo
                iPendencia.remetente    = iNomeRemetente
                iPendencia.idEstado     = iListaPendencias[i].versao.estado.id_estado_da_versao
                iLista.append(iPendencia)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaPendenciasDestinatario: ' + str(e))
            return False
        
    def adicionarFeedback(self, vIDVersao, vComentario):
        try:
            iPendencia= Pendencia.objects.filter(versao__id_versao= str(vIDVersao))[0]
            iPendencia.feedback= vComentario
            iPendencia.save()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel adicionarFeedback: ' + str(e))
            return False

class Workflow(models.Model):
    id_workflow     = models.IntegerField(max_length=5, primary_key=True)
    empresa         = models.ForeignKey(Empresa, unique=False)
    tipo_documento  = models.ForeignKey(Tipo_de_Documento, null= False)
    pasta           = models.ForeignKey(Pasta, null= False)
    descricao       = models.CharField(max_length=200, null= False)
    
    class Meta:
        db_table= 'tb_workflow'
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflow'
    
    def __unicode__(self):
        return str(self.id_workflow)
    
class Etapa_do_Workflow(models.Model):
    id_etapa_do_workflow    = models.IntegerField(max_length=5, primary_key=True)
    workflow                = models.ForeignKey(Workflow, null= False)
    grupo                   = models.ForeignKey(Grupo, null= False)
    tipo_de_pendencia       = models.ForeignKey(Tipo_de_Pendencia, null= False)
    eh_multiplo             = models.BooleanField(null= False, verbose_name='Multiplo', help_text='Indica que todos os usuários de determinado grupo devem efetuar a ação desejada.')
    descricao               = models.CharField(max_length=200, null= False)
    
    class Meta:
        db_table= 'tb_etapa_do_workflow'
        verbose_name = 'Etapa do Workflow'
        verbose_name_plural = 'Etapas do Workflow'
    
    def __unicode__(self):
        return str(self.id_etapa_do_workflow)