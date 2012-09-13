# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from autenticacao.models                import Empresa #@UnresolvedImport
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED                      import constantes

import logging
import os

#-----------------------------PASTA----------------------------------------

class Pasta(models.Model):
    id_pasta        = models.IntegerField(max_length=3, primary_key=True)
    pasta_pai       = models.ForeignKey('self', null=True)
    empresa         = models.ForeignKey(Empresa, null= False)
    nome            = models.CharField(max_length=30, null=False)
    diretorio       = models.CharField(max_length=200, null=False)
    
    class Meta:
        db_table= 'tb_pasta'
        verbose_name = 'Pasta'
        verbose_name_plural = 'Pastas'
    
    def __unicode__(self):
        return self.nome
    
    def save(self, vCriaPasta=True):  
        if self.id_pasta == '' or self.id_pasta== None:
            if len(Pasta.objects.order_by('-id_pasta')) > 0:   
                iUltimoRegistro = Pasta.objects.order_by('-id_pasta')[0] 
                self.id_pasta= iUltimoRegistro.pk + 1
            else:
                self.id_pasta= 1
            self.diretorio= self.montaDiretorioPasta(self.empresa.id_empresa, 
                                                               self, 
                                                               self.pasta_pai)
            if vCriaPasta:
                iDiretorioEmpresa   = constantes.cntConfiguracaoDiretorioDocumentos % self.empresa.id_empresa
                iDiretorio          = '%s/%s' % (iDiretorioEmpresa, self.diretorio)
                os.system('mkdir %s' % iDiretorio ) 
        super(Pasta, self).save()
    
    def criaPasta(self, vEmpresa, vNomePasta, vPastaPai=None):
        try:
            iPasta          = Pasta()
            iPasta.nome     = vNomePasta
            iPasta.empresa  = vEmpresa
            if vPastaPai != None:
                iPasta.pasta_pai= vPastaPai
            iPasta.save()
            return iPasta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar as pastas: ' + str(e))
            return False

    def obtemDiretorioUpload(self, vIDPasta, vIDEmpresa):
        try :
            iPasta = Pasta.objects.filter(id_pasta= vIDPasta)[0]
            iEmpresa= Empresa.objects.filter(id_empresa= vIDEmpresa)[0]
            iCaminho= '%s/%s' % (iEmpresa.pasta_raiz, iPasta.diretorio) 
            return iCaminho
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemDiretorioUpload: ' + str(e))
            return False
    
    def montaDiretorioPasta(self, vIDEmpresa, vPasta, vPastaPai=None):
        try :
            if vPastaPai == None:
                iDiretorio= '%s' % vPasta.id_pasta
            else:
                iPastaPai = Pasta.objects.filter(id_pasta= vPastaPai.id_pasta)[0]
                iDiretorio= '%s/%s' % (iPastaPai.diretorio, vPasta.id_pasta)
            return iDiretorio
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel omontar o Diretorio da Pasta: ' + str(e))
            return False
    
    def obtemNomeDaPasta(self, vIDPasta):
        try:
            iPasta = Pasta.objects.filter(id_pasta= vIDPasta)[0]
            return iPasta.nome
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de documentos: ' + str(e))
            return False

#-----------------------------GRUPO----------------------------------------

class Grupo(models.Model):
    id_grupo        = models.IntegerField(max_length=3, primary_key=True)
    nome            = models.CharField(max_length=100)
    descricao       = models.CharField(max_length=100)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_grupo'
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if self.id_grupo == None:
            if len(Grupo.objects.order_by('-id_grupo')) > 0:   
                iUltimoRegistro = Grupo.objects.order_by('-id_grupo')[0] 
                self.id_grupo= iUltimoRegistro.pk + 1
            else:
                self.id_grupo= 1
        super(Grupo, self).save()
        
    def criaGrupo(self, vEmpresa, vDescricao, vNome):
        try:
            iGrupo= Grupo()
            iGrupo.nome= vNome
            iGrupo.empresa= vEmpresa
            iGrupo.descricao= vDescricao
            iGrupo.save()
            return iGrupo
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os grupos: ' + str(e))
            return False
        
#-----------------------------GRUPO/PASTA------------------------------------        
        
class Grupo_Pasta(models.Model):
    id_grupo_pasta          = models.IntegerField(max_length=3, primary_key=True)
    grupo                   = models.ForeignKey(Grupo, null= False)
    pasta                   = models.ForeignKey(Pasta, null= False)
    
    class Meta:
        db_table= 'tb_grupo_pasta'
        verbose_name = 'Associar Grupo a Pasta'
        verbose_name_plural = 'Associar Grupo a Pasta'
    
    def __unicode__(self):
        return str(self.id_grupo_pasta)
    
    def save(self):  
        if self.id_grupo_pasta == None:
            if len(Grupo_Pasta.objects.order_by('-id_grupo_pasta')) > 0:   
                iUltimoRegistro = Grupo_Pasta.objects.order_by('-id_grupo_pasta')[0] 
                self.id_grupo_pasta= iUltimoRegistro.pk + 1
            else:
                self.id_grupo_pasta= 1
        super(Grupo_Pasta, self).save()
        
    def criaGrupo_Pasta(self, vGrupo, vPasta, vEmpresa):
        try:
            iGrupo_Pasta        = Grupo_Pasta()
            iGrupo_Pasta.grupo  = vGrupo
            iGrupo_Pasta.pasta  = vPasta
            iGrupo_Pasta.save()
            return iGrupo_Pasta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Grupo_Pasta: ' + str(e))
            return False
        
    def obtemListaGrupoPasta(self, vGrupo):
        try:
            iLista = Grupo_Pasta.objects.filter(grupo= vGrupo)[0]
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem lista GrupoPasta: ' + str(e))
            return False
        
    def possuiAcessoPasta(self, vUsuario, vIDPasta):
        try:
            iGrupoUsuario   = Grupo_Usuario().obtemGrupoUsuario(vUsuario)
            iLista          = Grupo_Pasta.objects.filter(grupo= iGrupoUsuario.grupo.id_grupo)
            iPossuiAcesso   = False
            for i in range(len(iLista)):
                if int(vIDPasta) == int(iLista[i].pasta.id_pasta):
                    iPossuiAcesso= True
            return iPossuiAcesso
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel possui Acesso Pasta: ' + str(e))
            return False
        
#-----------------------------GRUPO/USUARIO---------------------------------  
        
class Grupo_Usuario(models.Model):
    id_grupo_usuario        = models.IntegerField(max_length=3, primary_key=True)
    grupo                   = models.ForeignKey(Grupo, null= False)
    usuario                 = models.ForeignKey(Usuario, null= False)
    
    class Meta:
        db_table= 'tb_grupo_usuario'
        verbose_name = 'Associar Grupo a Usuário'
        verbose_name_plural = 'Associar Grupo a Usuário'
    
    def __unicode__(self):
        return str(self.id_grupo_usuario)
    
    def save(self):  
        if self.id_grupo_usuario == None:
            if len(Grupo_Usuario.objects.order_by('-id_grupo_usuario')) > 0:   
                iUltimoRegistro = Grupo_Usuario.objects.order_by('-id_grupo_usuario')[0] 
                self.id_grupo_usuario= iUltimoRegistro.pk + 1
            else:
                self.id_grupo_usuario= 1
        super(Grupo_Usuario, self).save()
        
    def criaGrupo_Usuario(self, vGrupo, vUsuario):
        try:
            iGrupo_Usuario        = Grupo_Usuario()
            iGrupo_Usuario.grupo  = vGrupo
            iGrupo_Usuario.usuario= vUsuario
            iGrupo_Usuario.save()
            return iGrupo_Usuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Grupo_Usuario: ' + str(e))
            return False
        
    def obtemGrupoUsuario(self, vUsuario):
        try:
            iGrupoUsuario = Grupo_Usuario.objects.filter(usuario= vUsuario.id)[0]
            return iGrupoUsuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem GruposUsuario: ' + str(e))
            return False
    
#-----------------------------FUNCAO----------------------------------------

class Funcao(models.Model):
    id_funcao       = models.IntegerField(max_length=3, primary_key=True)
    nome            = models.CharField(max_length=100)
    descricao       = models.CharField(max_length=100)
    
    class Meta:
        db_table= 'tb_funcao'
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if len(Funcao.objects.order_by('-id_funcao')) > 0:   
            iUltimoRegistro = Funcao.objects.order_by('-id_funcao')[0] 
            self.id_funcao= iUltimoRegistro.pk + 1
        else:
            self.id_funcao= 1
        super(Funcao, self).save()
        
    def criaFuncao(self, vNome, vDescricao):
        try:
            iFuncao             = Funcao()
            iFuncao.nome        = vNome
            iFuncao.descricao   = vDescricao
            iFuncao.save()
            return iFuncao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Funcao: ' + str(e))
            return False

class Funcao_Grupo(models.Model):
    id_funcao_grupo         = models.IntegerField(max_length=3, primary_key=True)
    funcao                  = models.ForeignKey(Funcao, null= False)
    grupo                   = models.ForeignKey(Grupo, null= False)
    
    
    class Meta:
        db_table= 'tb_funcao_grupo'
        verbose_name = 'Associar Função a Grupo'
        verbose_name_plural = 'Associar Função a Grupo'
    
    def __unicode__(self):
        return str(self.id_funcao_grupo)
    
    def save(self):  
        if self.id_funcao_grupo == None:
            if len(Funcao_Grupo.objects.order_by('-id_funcao_grupo')) > 0:   
                iUltimoRegistro = Funcao_Grupo.objects.order_by('-id_funcao_grupo')[0] 
                self.id_funcao_grupo= iUltimoRegistro.pk + 1
            else:
                self.id_funcao_grupo= 1
        super(Funcao_Grupo, self).save()
        
    def criaFuncao_Grupo(self, vFuncao, vGrupo):
        try:
            iFuncao_Grupo       = Funcao_Grupo()
            iFuncao_Grupo.funcao= vFuncao
            iFuncao_Grupo.grupo = vGrupo
            iFuncao_Grupo.save()
            return iFuncao_Grupo
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Funcao_Grupo: ' + str(e))
            return False
        
    def obtemListaFuncaoGrupo(self, vGrupo):
        try:
            iListaFuncoes = Funcao_Grupo.objects.filter(grupo= vGrupo)
            return iListaFuncoes
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem lista FuncoesGrupo: ' + str(e))
            return False
        
    def possuiAcessoFuncao(self, vUsuario, vIDFuncao):
        try:
            iGrupoUsuario   = Grupo_Usuario().obtemGrupoUsuario(vUsuario)
            iLista          = Funcao_Grupo.objects.filter(grupo= iGrupoUsuario.grupo.id_grupo)
            iPossuiAcesso   = False
            for i in range(len(iLista)):
                if int(vIDFuncao) == int(iLista[i].funcao.id_funcao):
                    iPossuiAcesso= True
            return iPossuiAcesso
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel possui Acesso Funcao: ' + str(e))
            return False
        
#-----------------------------IPs_PERMETIDOS----------------------------------------

class Firewall(models.Model):
    id_firewall     = models.IntegerField(max_length=3, primary_key=True)
    ip              = models.CharField(max_length=20)
    descricao       = models.CharField(max_length=100)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_firewall'
        verbose_name = 'Firewall'
        verbose_name_plural = 'Firewall'
    
    def __unicode__(self):
        return self.ip
    
    def save(self):  
        if self.id_firewall == None:
            if len(Firewall.objects.order_by('-id_firewall')) > 0:   
                iUltimoRegistro = Firewall.objects.order_by('-id_firewall')[0] 
                self.id_firewall= iUltimoRegistro.pk + 1
            else:
                self.id_firewall= 1
        super(Firewall, self).save()
        
    def verificaIP (self, vIP, vEmpresa):
        try :
            iPossivel= False
            iListaFirewall= Firewall.objects.filter(empresa= vEmpresa)
            if len(iListaFirewall) == 0:
                return True
            iListaIP= vIP.split('.')
            for i in range(len(iListaFirewall)):
                iFirewall= iListaFirewall[i].ip.split('.')
                if iListaIP[0] == iFirewall[0] and iListaIP[1] == iFirewall[1] and iListaIP[2] == iFirewall[2] and iListaIP[3] == iFirewall[3]:
                    iPossivel=True
                elif iFirewall[2] == '0' and iFirewall[3] == '0':
                    if iListaIP[0] == iFirewall[0] and iListaIP[1] == iFirewall[1]:
                        iPossivel=True
            return iPossivel
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel verificar IP: ' + str(e))
            return False

class Firewall_Grupo(models.Model):
    id_firewall_grupo       = models.IntegerField(max_length=3, primary_key=True)
    firewall                = models.ForeignKey(Firewall, null= False)
    grupo                   = models.ForeignKey(Grupo, null= False)
    
    class Meta:
        db_table= 'tb_firewall_grupo'
        verbose_name = 'Associar Firewall a Grupo'
        verbose_name_plural = 'Associar Firewall a Grupo'
    
    def __unicode__(self):
        return str(self.id_firewall_grupo)
    
    def save(self):  
        if self.id_firewall_grupo == None:
            if len(Firewall_Grupo.objects.order_by('-id_firewall_grupo')) > 0:   
                iUltimoRegistro = Firewall_Grupo.objects.order_by('-id_firewall_grupo')[0] 
                self.id_firewall_grupo= iUltimoRegistro.pk + 1
            else:
                self.id_firewall_grupo= 1
        super(Firewall_Grupo, self).save()
