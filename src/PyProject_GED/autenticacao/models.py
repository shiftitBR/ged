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
                iPastaRaiz= mPasta().criaPasta(vEmpresa, 'Pasta Raiz')
                iPastaModelo= mPasta().criaPasta(vEmpresa, 'Modelos', iPastaRaiz)
                mTipoDocumento().criaTipoDocumento(vEmpresa, 'Modelo')
                ControleAutenticacao().criaPasta(vEmpresa.id_empresa, 
                                                 iPastaRaiz.id_pasta, 
                                                 iPastaModelo.id_pasta)
        try:
            iThread = ThreadClass()
            iThread.start()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a Empresa: ' + str(e))
            return False
        
    def obtemListaEnderecoEmpresas(self):
        try:
            iEmpresas= Empresa.objects.filter()
            iLista= ''
            for i in range(len(iEmpresas)):
                if (iEmpresas[i].rua != '' or iEmpresas[i].bairro != '') and (iEmpresas[i].rua != None or iEmpresas[i].bairro != None):
                    iInfo= "%s %s %s %s %s %s" % (iEmpresas[i].rua, str(iEmpresas[i].numero), iEmpresas[i].cep, iEmpresas[i].bairro, iEmpresas[i].cidade, iEmpresas[i].uf)
                    if iLista== '':
                        iLista= str(iEmpresas[i].id_empresa) + '%' + iInfo + '%' + str(iEmpresas[i].nome)
                    else:
                        iLista= iLista + '%' + str(iEmpresas[i].id_empresa) + '%' + iInfo + '%' + str(iEmpresas[i].nome)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter obtemListaEnderecoEmpresas ' + str(e))
            return False 
        
        
#---------------------------USUARIO -----------------------------------
        
class Tipo_de_Usuario(models.Model):
    id_tipo_de_usuario  = models.IntegerField(max_length=3, primary_key=True)
    descricao           = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_tipo_de_usuario'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Tipo_de_Usuario.objects.order_by('-id_tipo_de_usuario')) > 0:   
            iUltimoRegistro = Tipo_de_Usuario.objects.order_by('-id_tipo_de_usuario')[0] 
            self.id_tipo_de_usuario= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_de_usuario= 1
        super(Tipo_de_Usuario, self).save()
    
    
class Usuario(User):
    empresa         = models.ForeignKey(Empresa, null= False)
    tipo_usuario    = models.ForeignKey(Tipo_de_Usuario, null= False)
    
    class Meta:
        db_table= 'tb_usuario'
    
    def __unicode__(self):
        return self.username
    
    def save(self): 
        if self.username == '':
            if len(User.objects.order_by('-id')) > 0:   
                iUltimoRegistro = User.objects.order_by('-id')[0] 
                self.username= "%03d-%06d" % (int(self.empresa.pk), int(iUltimoRegistro.pk) + 1)
            else:
                self.username= "%03d-%06d" % (int(self.empresa.pk), 1)
        if not self.comaparaSenha(self.pk, self.password):
            self.set_password(self.password)   
        super(Usuario, self).save()   
    
    def comaparaSenha(self, vIDUsuario, vSenha):
        try:
            try:
                iUsuario= Usuario.objects.filter(pk= vIDUsuario)[0]
            except:
                return False
            if iUsuario.password == vSenha:
                return True
            else:
                return False
            return iUsuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel comparar a senha do usuario ' + str(e))
            return False 
        
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
        
    def obterNomeUsuario(self, vIDUsuario):
        try:
            iUsuario= Usuario.objects.filter(id= vIDUsuario)[0]
            iNome= iUsuario.first_name + ' ' + iUsuario.last_name[:1] + '.'
            return iNome
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o nome do usuario ' + str(e))
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
    
    def obtemUsuariosDaEmpresa(self, vEmpresa):
        try:
            iListaUsuarios= Usuario.objects.filter(empresa= vEmpresa)
            return iListaUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter os Usuarios da empresa ' + str(e))
            return False 
    
    def obtemUsuariosComEmailDaEmpresa(self, vEmpresa):
        try:
            iListaUsuarios= Usuario.objects.filter(empresa= vEmpresa).filter(
                                tipo_usuario__id_tipo_de_usuario= constantes.cntTipoUsuarioSistema).filter(email__isnull=False)
            return iListaUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter os Usuarios da empresa ' + str(e))
            return False 
        
    def obtemContatosComEmailDaEmpresa(self, vEmpresa):
        try:
            iListaUsuarios= Usuario.objects.filter(empresa= vEmpresa).filter(
                                tipo_usuario__id_tipo_de_usuario= constantes.cntTipoUsuarioContato).filter(email__isnull=False)
            return iListaUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter os Usuarios da empresa ' + str(e))
            return False    
    
    def obtemUsuariosPeloTipo(self, vEmpresa, vIDTipoUsuario):
        try:
            iTipoUsuario    = Tipo_de_Usuario.objects.filter(empresa= vEmpresa).filter(id_tipo_de_usuario= vIDTipoUsuario)
            iUsuarios       = Usuario.objects.filter(tipo_usuario= iTipoUsuario)
            return iUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o Usuario pelo tipo de usuario ' + str(e))
            return False  
