# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from django.contrib.auth.models         import User
from django.conf                        import settings
from django.db.models                   import get_model
from controle                           import Controle as ControleAutenticacao

import constantes #@UnresolvedImport
import threading
import logging
import time

from PyProject_GED.autenticacao.controle import Controle

#-----------------------------EMPRESA---------------------------------------

class Empresa(models.Model):
    id_empresa      = models.IntegerField(max_length=3, primary_key=True, null= False, blank=True)
    nome            = models.CharField(max_length=50, null= False)
    cnpj            = models.CharField(max_length=15, null= True, blank=True)
    ddd             = models.CharField(max_length=2, null= True, blank=True)
    telefone        = models.CharField(max_length=15, null= True, blank=True)
    cep             = models.CharField(max_length=15, null= True, blank=True)
    rua             = models.CharField(max_length=50, null= True, blank=True)
    numero          = models.CharField(max_length=10, null= True, blank=True)
    complemento     = models.CharField(max_length=40, null= True, blank=True)
    bairro          = models.CharField(max_length=30, null= True, blank=True)
    cidade          = models.CharField(max_length=30, null= True, blank=True)
    uf              = models.CharField(max_length=2, null= True, blank=True)
    pasta_raiz      = models.CharField(max_length=100, null= False, blank=True)
    eh_ativo        = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_empresa'
    
    def __unicode__(self):
        return "%s - %s" % (str(self.id_empresa), self.nome)
    
    def save(self, vCriaEmpresa=True):  
        iEmpresaNova= False
        if self.id_empresa == None: 
            iEmpresaNova= True
            if len(Empresa.objects.order_by('-id_empresa')) > 0:   
                iUltimoRegistro = Empresa.objects.order_by('-id_empresa')[0] 
                self.id_empresa= iUltimoRegistro.pk + 1
            else:
                self.id_empresa= 1
        self.pasta_raiz= '%s/media/%s/empresa_%03d' % (settings.PROJECT_ROOT_PATH, 
                                                 settings.MULTI_IMAGES_FOLDER, 
                                                 int(self.id_empresa))     
        super(Empresa, self).save()
        if vCriaEmpresa and iEmpresaNova:
            self.criaEmpresa(self)
    
    def criaEmpresa(self, vEmpresa):
        class ThreadClass(threading.Thread):
            def run(self):
                time.sleep(1)
                mPasta= get_model('seguranca', 'Pasta')
                mTipoDocumento= get_model('documento', 'Tipo_de_Documento')
                mTipoDeIndice= get_model('indice', 'Tipo_de_Indice')
                iPastaRaiz= mPasta().criaPasta(vEmpresa, 'Pasta Raiz')
                iPastaModelo= mPasta().criaPasta(vEmpresa, 'Modelos', iPastaRaiz)
                Tipo_de_Usuario().criaTipoUsuario(vEmpresa, 'Administrador')
                mTipoDeIndice().criaTipoIndice(vEmpresa, 'String')
                mTipoDocumento().criaTipoDocumento(vEmpresa, 'Modelo')
                ControleAutenticacao().criaPasta(vEmpresa.id_empresa, 
                                                 iPastaRaiz.id_pasta, 
                                                 iPastaModelo.id_pasta)
        try:
            iThread = ThreadClass()
            iThread.start()
            return True
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a Empresa: ' + str(e))
            return False

#---------------------------USUARIO---------------------------------------

class Tipo_de_Usuario(models.Model):
    id_tipo_usuario     = models.IntegerField(max_length=3, primary_key=True, blank=True)
    descricao           = models.CharField(max_length=30)
    empresa             = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_tipo_de_usuario'
    
    def __unicode__(self):
        return '%s [%s]' % (self.descricao, self.empresa.nome)
    
    def save(self):  
        if len(Tipo_de_Usuario.objects.order_by('-id_tipo_usuario')) > 0:   
            iUltimoRegistro = Tipo_de_Usuario.objects.order_by('-id_tipo_usuario')[0] 
            self.id_tipo_usuario= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_usuario= 1
        super(Tipo_de_Usuario, self).save()
    
    def criaTipoUsuario(self, vEmpresa, vDescricao):
        try:
            iTipoUsuario= Tipo_de_Usuario()
            iTipoUsuario.descricao= vDescricao
            iTipoUsuario.empresa= vEmpresa
            iTipoUsuario.save()
            return iTipoUsuario
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os tipos de usuario: ' + str(e))
            return False
    
    def obtemListaDeAdministradores(self):
        try:
            iListaEmpresa= Empresa.objects.all()
            iListaIDAdministradores= []
            for i in range(len(iListaEmpresa)):
                iListaTiposDaEmpresa= Tipo_de_Usuario.objects.filter(empresa= iListaEmpresa[i]).order_by('empresa')
                if len(iListaTiposDaEmpresa) > 0:
                    iListaIDAdministradores.append(iListaTiposDaEmpresa[0].id_tipo_usuario) 
            return iListaIDAdministradores
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter lista de Administradores: ' + str(e))
            return False

class Usuario(User):
    empresa         = models.ForeignKey(Empresa, null= False)
    tipo_usuario    = models.ForeignKey(Tipo_de_Usuario, null= False)
    eh_ativo        = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_usuario'
    
    def __unicode__(self):
        return self.username
    
    def save(self): 
        if self.username == '':
            if len(User.objects.using(constantes.cntConfiguracaoBancoPadrao).order_by('-id')) > 0:   
                iUltimoRegistro = User.objects.using(constantes.cntConfiguracaoBancoPadrao).order_by('-id')[0] 
                self.username= "%03d-%06d" % (int(self.empresa.pk), int(iUltimoRegistro.pk) + 1)
            else:
                self.username= "%03d-%06d" % (int(self.empresa.pk), 1)
        self.set_password(self.password)   
        super(Usuario, self).save()   
        
    def obtemUsuario(self, vUser):
        try:
            iUsuario= Usuario.objects.filter(pk= vUser.pk)[0]
            return iUsuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o Usuario pelo user ' + str(e))
            return False 
    
    def obtemUsuarioPeloID(self, vIDUsuario):
        try:
            iUsuario= Usuario.objects.filter(id= vIDUsuario)[0]
            return iUsuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o Usuario pelo user ' + str(e))
            return False   

    def obtemEmpresaDoUsuario(self, vIDUsario):
        try:
            iListaUsuarios= Usuario.objects.filter(pk= vIDUsario)
            if len(iListaUsuarios) > 0:
                return iListaUsuarios[0].empresa
            else:
                return None
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a Empresa do Usuario ' + str(e))
            return False 