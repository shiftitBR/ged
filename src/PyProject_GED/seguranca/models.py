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

    def ehPastaRaiz(self, vIDPasta, vIDEmpresa):
        try:
            iPastaRaiz = Pasta.objects.filter(empresa=vIDEmpresa).order_by('id_pasta')[0]
            if str(iPastaRaiz.id_pasta) == vIDPasta:
                return True
            else:
                return False
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel eh Pasta Raiz: ' + str(e))
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
        
    def criaGrupo_Pasta(self, vGrupo, vPasta, vEmpresa=None, vPastaID=None, vGrupoID=None):
        try:
            if vPastaID != None:
                iPasta= Pasta.objects.filter(id_pasta= int(vPastaID))[0]
            else:
                iPasta= vPasta
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            iGrupo_Pasta        = Grupo_Pasta()
            iGrupo_Pasta.grupo  = iGrupo
            iGrupo_Pasta.pasta  = iPasta
            iGrupo_Pasta.save()
            return iGrupo_Pasta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Grupo_Pasta: ' + str(e))
            return False
        
    def excluiPastasDoGrupo(self, vGrupo, vGrupoID=None):
        try:
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            Grupo_Pasta.objects.filter(grupo= iGrupo).delete()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel excluir pastas do grupo: ' + str(e))
            return False 
    
    def obtemListaGrupoPasta(self, vGrupo):
        try:
            iLista = Grupo_Pasta.objects.filter(grupo= vGrupo)
            return iLista
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem lista GrupoPasta: ' + str(e))
            return False
    
    def obtemListaDeGruposSemPasta(self, vEmpresa=None):
        try:
            iListaGrupos    = Grupo.objects.all()
            iListaGruposPasta     = Grupo_Pasta.objects.all()
            if vEmpresa != None:
                iListaGrupos    = iListaGrupos.filter(empresa= vEmpresa)
                iListaGruposPasta     = iListaGruposPasta.filter(grupo__empresa= vEmpresa)
            iListaGruposSemPastas     = []
            iListaGruposComPastas     = []
            for iGrupoPasta in iListaGruposPasta:
                iListaGruposComPastas.append(iGrupoPasta.grupo)
            for iGrupo in iListaGrupos:
                if iGrupo not in iListaGruposComPastas:
                    iListaGruposSemPastas.append(iGrupo)
            return iListaGruposSemPastas
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem lista FuncoesGrupo: ' + str(e))
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
        
    def criaGrupo_Usuario(self, vGrupo, vUsuario, vUsuarioID=None, vGrupoID=None):
        try:
            if vUsuarioID != None:
                iUsuario= Usuario.objects.filter(id= int(vUsuarioID))[0]
            else:
                iUsuario= vUsuario
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            iGrupo_Usuario        = Grupo_Usuario()
            iGrupo_Usuario.grupo  = iGrupo
            iGrupo_Usuario.usuario= iUsuario
            iGrupo_Usuario.save()
            return iGrupo_Usuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Grupo_Usuario: ' + str(e))
            return False  
    
    def excluiUsuariosDoGrupo(self, vGrupo, vGrupoID=None):
        try:
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            Grupo_Usuario.objects.filter(grupo= iGrupo).delete()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel excluir usuarios do grupo: ' + str(e))
            return False      
        
    def obtemGrupoUsuario(self, vUsuario):
        try:
            iGrupoUsuario = Grupo_Usuario.objects.filter(usuario= vUsuario.id)[0]
            return iGrupoUsuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem GruposUsuario: ' + str(e))
            return False
    
    def obtemListaDeGruposSemUsuario(self, vEmpresa=None):
        try:
            iListaGrupos    = Grupo.objects.all()
            iListaGruposUsuario     = Grupo_Usuario.objects.all()
            if vEmpresa != None:
                iListaGrupos    = iListaGrupos.filter(empresa= vEmpresa)
                iListaGruposUsuario     = iListaGruposUsuario.filter(grupo__empresa= vEmpresa)
            iListaGruposSemUsuarios     = []
            iListaGruposComUsuarios     = []
            for iGrupoUsuario in iListaGruposUsuario:
                iListaGruposComUsuarios.append(iGrupoUsuario.grupo)
            for iGrupo in iListaGrupos:
                if iGrupo not in iListaGruposComUsuarios:
                    iListaGruposSemUsuarios.append(iGrupo)
            return iListaGruposSemUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem lista FuncoesGrupo: ' + str(e))
            return False
    
    def obtemUsuariosDisponiveis(self, vEmpresa=None, vGrupo=None):
        try:
            iListaUsuarios= Usuario().obtemUsuariosPeloTipo(vEmpresa, constantes.cntTipoUsuarioSistema)
            iListaGrupoUsuario= Grupo_Usuario.objects.all()
            iListaUsuariosDoGrupo = []
            if vEmpresa != None:
                iListaGrupoUsuario= iListaGrupoUsuario.filter(grupo__empresa= vEmpresa)
            if vGrupo != None:
                iListaUsuariosDoGrupo  = self.obtemUsuariosDoGrupo(vGrupo)
            iListaUsuariosComGrupo= []
            iListaIDsUsuariosSemGrupo= []
            for iGrupoUsuario in iListaGrupoUsuario:
                iListaUsuariosComGrupo.append(iGrupoUsuario.usuario)
            for iUsuario in iListaUsuarios:
                if iUsuario not in iListaUsuariosComGrupo:
                    iListaIDsUsuariosSemGrupo.append(iUsuario.id)
            iListaUsuariosDoGrupo  = self.obtemUsuariosDoGrupo(vGrupo)
            for iUsuario in iListaUsuariosDoGrupo:
                iListaIDsUsuariosSemGrupo.append(iUsuario.id)
            iListaUsuariosSemGrupo = Usuario.objects.filter(id__in= iListaIDsUsuariosSemGrupo)
            return iListaUsuariosSemGrupo
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter lista de usuarios disponiveis: ' + str(e))
            return False
    
    def obtemUsuariosDoGrupo(self, vGrupo):
        try:
            iListaGrupoUsuario= Grupo_Usuario.objects.filter(grupo= vGrupo)
            iListaIDUsuarios= []
            for iGrupoUsuario in iListaGrupoUsuario:
                iListaIDUsuarios.append(iGrupoUsuario.usuario.id)
            iListaUsuarios= Usuario.objects.filter(id__in= iListaIDUsuarios)
            return iListaUsuarios
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter lista de usuarios do grupo: ' + str(e))
            return False
    
    def obtemPastasPermitidasDoUsuario(self, vIDUsuario):
        try:
            iUsuario= Usuario().obtemUsuarioPeloID(vIDUsuario)
            iGrupoUsuario= self.obtemGrupoUsuario(iUsuario)
            iListaDeGrupoPasta= Grupo_Pasta().obtemListaGrupoPasta(iGrupoUsuario.grupo)
            iListaDePastas= []
            for iGrupoPasta in iListaDeGrupoPasta:
                iListaDePastas.append(iGrupoPasta.pasta)
            return iListaDePastas
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter lista de pastas permitidas: ' + str(e))
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
        
    def criaFuncao_Grupo(self, vFuncao, vGrupo, vFuncaoID=None, vGrupoID=None):
        try:
            if vFuncaoID != None:
                iFuncao= Funcao.objects.filter(id_funcao= int(vFuncaoID))[0]
            else:
                iFuncao= vFuncao
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            iFuncao_Grupo       = Funcao_Grupo()
            iFuncao_Grupo.funcao= iFuncao
            iFuncao_Grupo.grupo = iGrupo
            iFuncao_Grupo.save()
            return iFuncao_Grupo
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Funcao_Grupo: ' + str(e))
            return False
    
    def excluiFuncoesDoGrupo(self, vGrupo, vGrupoID=None):
        try:
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            Funcao_Grupo.objects.filter(grupo= iGrupo).delete()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel excluir funcoes do grupo: ' + str(e))
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
    
    def obtemListaDeGruposSemFuncao(self, vEmpresa=None):
        try:
            iListaGrupos    = Grupo.objects.all()
            iListaGruposFuncoes     = Funcao_Grupo.objects.all()
            if vEmpresa != None:
                iListaGrupos    = iListaGrupos.filter(empresa= vEmpresa)
                iListaGruposFuncoes     = iListaGruposFuncoes.filter(grupo__empresa= vEmpresa)
            iListaGruposSemFuncao   = []
            iListaGruposComFuncoes  = []
            for iGrupoFuncao in iListaGruposFuncoes:
                iListaGruposComFuncoes.append(iGrupoFuncao.grupo)
            for iGrupo in iListaGrupos:
                if iGrupo not in iListaGruposComFuncoes:
                    iListaGruposSemFuncao.append(iGrupo)
            return iListaGruposSemFuncao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtem lista FuncoesGrupo: ' + str(e))
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
    
    def criaFirewall_Grupo(self, vGrupo, vFirewall, vFirewallID=None, vGrupoID=None):
        try:
            if vFirewallID != None:
                iFirewall= Firewall.objects.filter(id_firewall= int(vFirewallID))[0]
            else:
                iFirewall= vFirewall
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            iFirewall_Grupo         = Firewall_Grupo()
            iFirewall_Grupo.grupo   = iGrupo
            iFirewall_Grupo.firewall= iFirewall
            iFirewall_Grupo.save()
            return iFirewall_Grupo
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Firewall_Grupo: ' + str(e))
            return False  
    
    def excluiFirewallsDoGrupo(self, vGrupo, vGrupoID=None):
        try:
            if vGrupoID != None:
                iGrupo= Grupo.objects.filter(id_grupo= int(vGrupoID))[0]
            else:
                iGrupo= vGrupo
            Firewall_Grupo.objects.filter(grupo= iGrupo).delete()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel excluir firewalls do grupo: ' + str(e))
            return False
    
    def obtemListaDeGruposSemFirewall(self, vEmpresa=None):
        try:
            iListaGrupos            = Grupo.objects.all()
            iListaFirewallsGrupo    = Firewall_Grupo.objects.all()
            if vEmpresa != None:
                iListaGrupos          = iListaGrupos.filter(empresa= vEmpresa)
                iListaFirewallsGrupo   = iListaFirewallsGrupo.filter(grupo__empresa= vEmpresa)
            iListaGruposSemFirewall   = []
            iListaGruposComFirewall   = []
            for iFirewallGrupo in iListaFirewallsGrupo:
                iListaGruposComFirewall.append(iFirewallGrupo.grupo)
            for iGrupo in iListaGrupos:
                if iGrupo not in iListaGruposComFirewall:
                    iListaGruposSemFirewall.append(iGrupo)
            return iListaGruposSemFirewall
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter lista de grupos sem firewall: ' + str(e))
            return False
