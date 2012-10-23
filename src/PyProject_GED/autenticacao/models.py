# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                                      import models
from django.contrib.auth.models                     import User
from django.conf                                    import settings
from django.db.models                               import get_model
from controle                                       import Controle as ControleAutenticacao
from PyProject_GED.relatorios.objetos_auxiliares    import RelatorioUsuario as UsuarioAuxiliar
from PyProject_GED                                  import constantes
from django.contrib.auth                            import authenticate 

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
    eh_ativo        = models.BooleanField(null= False, verbose_name='Ativa', help_text='Empresa Ativa')
    eh_publico      = models.BooleanField(null= False, verbose_name='Pública', help_text='Possui Documentos Públicos para Divulgação')
    
    class Meta:
        db_table= 'tb_empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
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
                ControleAutenticacao().criaPastaEmpresa(vEmpresa.id_empresa) 
                iPastaRaiz= mPasta().criaPasta(vEmpresa, 'Pasta Raiz')
                mPasta().criaPasta(vEmpresa, 'Modelos', iPastaRaiz)
                mTipoDocumento().criaTipoDocumento(vEmpresa, 'Modelo')
        try:
            iThread = ThreadClass()
            iThread.start()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a Empresa: ' + str(e))
            return False
        
    def obtemListaEnderecoEmpresas(self):
        try:
            iEmpresas= Empresa.objects.filter(eh_publico = True)
            iLista= ''
            for i in range(len(iEmpresas)):
                iRua    = unicode(iEmpresas[i].rua)
                iNumero = unicode(iEmpresas[i].numero)
                iCep    = unicode(iEmpresas[i].cep)
                iBairro = unicode(iEmpresas[i].bairro)
                iCidade = unicode(iEmpresas[i].cidade)
                iUF     = unicode(iEmpresas[i].uf)
                iInfo= "%s %s %s %s %s %s" % (iRua, iNumero, iCep, iBairro, iCidade, iUF)
                if iLista== '':
                    iLista= str(iEmpresas[i].id_empresa) + '%' + iInfo + '%' + unicode(iEmpresas[i].nome)
                else:
                    iLista= iLista + '%' + str(iEmpresas[i].id_empresa) + '%' + iInfo + '%' + unicode(iEmpresas[i].nome)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter obtemListaEnderecoEmpresas ' + str(e))
            return False 
        
    def obtemEmpresaPeloID(self, vIDEmpresa):
        try:
            iEmpresa= Empresa.objects.filter(id_empresa= vIDEmpresa)[0]
            return iEmpresa
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter Empresa pelo id' + str(e))
            return False   
        
#---------------------------USUARIO -----------------------------------
        
class Tipo_de_Usuario(models.Model):
    id_tipo_de_usuario  = models.IntegerField(max_length=3, primary_key=True)
    descricao           = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_tipo_de_usuario'
        verbose_name = 'Tipo de Usuário'
        verbose_name_plural = 'Tipos de Usuário'
    
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
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __unicode__(self):
        return "%s - %s %s" % (self.username, self.first_name, self.last_name)
    
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
        
    def adicionaContato(self, vEmpresa, vFirstName, vLastName, vEmail):
        try:
            iTipoContato = Tipo_de_Usuario.objects.filter(id_tipo_de_usuario= constantes.cntTipoUsuarioContato)[0]
            iContato = Usuario()
            iContato.first_name = vFirstName
            iContato.last_name  = vLastName
            iContato.email      = vEmail
            iContato.empresa    = vEmpresa
            iContato.tipo_usuario= iTipoContato
            iContato.save()
            return iContato
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel adiciona Contato ' + str(e))
            return False 
        
    def ehContato(self, vUsuario):
        try:
            iTipoContato = Tipo_de_Usuario.objects.filter(id_tipo_de_usuario= constantes.cntTipoUsuarioContato)[0]
            if vUsuario.tipo_usuario == iTipoContato:
                return True
            else:
                return False
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel eh Contato ' + str(e))
            return False
        
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
        
    def obtemUsuarioPeloEmail(self, vEmail):
        try:
            iListaUsuario= Usuario.objects.filter(email= vEmail)
            iUsuario= None
            for i in iListaUsuario:
                iUsuario= i
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
            iListaUsuarios= Usuario.objects.filter(empresa= vEmpresa).order_by('first_name')
            return iListaUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter os Usuarios da empresa ' + str(e))
            return False 
    
    def obtemUsuariosComEmailDaEmpresa(self, vEmpresa):
        try:
            iListaUsuarios= Usuario.objects.filter(empresa= vEmpresa).filter(email__isnull=False)
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
            iTipoUsuario    = Tipo_de_Usuario.objects.filter(id_tipo_de_usuario= vIDTipoUsuario)
            iUsuarios       = Usuario.objects.filter(empresa= vEmpresa).filter(tipo_usuario= iTipoUsuario)
            return iUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter o Usuario pelo tipo de usuario ' + str(e))
            return False  
        
    def obtemUsuariosRelatorio(self, vIDEmpresa, vIDTipoUsuario):
        try:
            iEmpresa        = Empresa().obtemEmpresaPeloID(vIDEmpresa)
            iTipoUsuario    = Tipo_de_Usuario.objects.filter(id_tipo_de_usuario= vIDTipoUsuario)
            iUsuarios       = Usuario.objects.filter(empresa= iEmpresa).filter(tipo_usuario= iTipoUsuario).order_by('id')
            iListaAux       = []
            for iUsuario in iUsuarios:
                iUsuarioAux = UsuarioAuxiliar()
                iUsuarioAux.id              = iUsuario.id
                iUsuarioAux.nome            = '%s %s' % (iUsuario.first_name, iUsuario.last_name)
                iUsuarioAux.username        = iUsuario.username
                iUsuarioAux.email           = iUsuario.email
                if iUsuario.is_active:
                    iUsuarioAux.ehAtivo     = 'Sim' 
                else:
                    iUsuarioAux.ehAtivo     = 'Nao'
                if iUsuario.is_superuser :
                    iUsuarioAux.ehAdministrador = 'Sim'
                else:
                    iUsuarioAux.ehAdministrador = 'Nao'
                iUsuarioAux.dataUltimoLogin = iUsuario.last_login.strftime('%Y-%m-%d')
                iUsuarioAux.dataCadastro    = iUsuario.date_joined.strftime('%Y-%m-%d')
                iListaAux.append(iUsuarioAux)
            return iListaAux
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem Usuarios Relatorio' + str(e))
            return False  
    
    def autenticaUsuario(self, vEmail, vSenha):
        try:
            iUsuario= authenticate(username=vEmail, password=vSenha)
            return iUsuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel autenticar o usuario' + str(e))
            return False  
