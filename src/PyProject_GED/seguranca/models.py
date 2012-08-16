'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from autenticacao.models                import Empresa #@UnresolvedImport

import logging

#-----------------------------PASTA----------------------------------------

class Pasta(models.Model):
    id_pasta        = models.IntegerField(max_length=3, primary_key=True)
    pasta_pai       = models.ForeignKey('self', null=True)
    empresa         = models.ForeignKey(Empresa, null= False)
    nome            = models.CharField(max_length=30, null=False)
    diretorio       = models.CharField(max_length=200, null=False)
    
    class Meta:
        db_table= 'tb_pasta'
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if len(Pasta.objects.order_by('-id_pasta')) > 0:   
            iUltimoRegistro = Pasta.objects.order_by('-id_pasta')[0] 
            self.id_pasta= iUltimoRegistro.pk + 1
        else:
            self.id_pasta= 1
        self.diretorio= self.montaDiretorioPasta(self.empresa.id_empresa, 
                                                               self, 
                                                               self.pasta_pai)
        super(Pasta, self).save()
    
    def criaPasta(self, vEmpresa, vNomePasta, vPastaPai=None):
        try:
            iPasta= Pasta()
            iPasta.id_pasta= 1
            iPasta.nome= vNomePasta
            iPasta.empresa= vEmpresa
            if vPastaPai != None:
                iPasta.pasta_pai= vPastaPai
            iPasta.save()
            return iPasta
        except Exception, e:
            print str(e)
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
                iDiretorio= '%s/%s' % (iPastaPai.id_pasta, vPasta.id_pasta)
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
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if len(Grupo.objects.order_by('-id_grupo')) > 0:   
            iUltimoRegistro = Grupo.objects.order_by('-id_grupo')[0] 
            self.id_grupo= iUltimoRegistro.pk + 1
        else:
            self.id_grupo= 1
        super(Grupo, self).save()
        
class Grupo_Pasta(models.Model):
    id_grupo_pasta          = models.IntegerField(max_length=3, primary_key=True)
    grupo                   = models.ForeignKey(Grupo, null= False)
    pasta                   = models.ForeignKey(Pasta, null= False)
    empresa                 = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_grupo_pasta'
    
    def __unicode__(self):
        return self.id_grupo_pasta
    
    def save(self):  
        if len(Grupo_Pasta.objects.order_by('-id_grupo_pasta')) > 0:   
            iUltimoRegistro = Grupo_Pasta.objects.order_by('-id_grupo_pasta')[0] 
            self.id_grupo_pasta= iUltimoRegistro.pk + 1
        else:
            self.id_grupo_pasta= 1
        super(Grupo_Pasta, self).save()
        
#-----------------------------FUNCAO----------------------------------------

class Funcao(models.Model):
    id_funcao       = models.IntegerField(max_length=3, primary_key=True)
    nome            = models.CharField(max_length=100)
    descricao       = models.CharField(max_length=100)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_funcao'
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if len(Funcao.objects.order_by('-id_funcao')) > 0:   
            iUltimoRegistro = Funcao.objects.order_by('-id_funcao')[0] 
            self.id_funcao= iUltimoRegistro.pk + 1
        else:
            self.id_funcao= 1
        super(Funcao, self).save()

class Funcao_Grupo(models.Model):
    id_funcao_grupo         = models.IntegerField(max_length=3, primary_key=True)
    funcao                  = models.ForeignKey(Funcao, null= False)
    grupo                   = models.ForeignKey(Grupo, null= False)
    
    
    class Meta:
        db_table= 'tb_funcao_grupo'
    
    def __unicode__(self):
        return self.id_funcao_grupo
    
    def save(self):  
        if len(Funcao_Grupo.objects.order_by('-id_funcao_grupo')) > 0:   
            iUltimoRegistro = Funcao_Grupo.objects.order_by('-id_funcao_grupo')[0] 
            self.id_funcao_grupo= iUltimoRegistro.pk + 1
        else:
            self.id_funcao_grupo= 1
        super(Funcao_Grupo, self).save()

#-----------------------------IPs_PERMETIDOS----------------------------------------

class Firewall(models.Model):
    id_firewall     = models.IntegerField(max_length=3, primary_key=True)
    ip              = models.CharField(max_length=20)
    descricao       = models.CharField(max_length=100)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_firewall'
    
    def __unicode__(self):
        return self.ip
    
    def save(self):  
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
    
    def __unicode__(self):
        return self.id_firewall_grupo
    
    def save(self):  
        if len(Firewall_Grupo.objects.order_by('-id_firewall_grupo')) > 0:   
            iUltimoRegistro = Firewall_Grupo.objects.order_by('-id_firewall_grupo')[0] 
            self.id_firewall_grupo= iUltimoRegistro.pk + 1
        else:
            self.id_firewall_grupo= 1
        super(Firewall_Grupo, self).save()
