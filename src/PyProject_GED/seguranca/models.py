'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models
from controle                   import Controle #@UnresolvedImport

#-----------------------------PASTA----------------------------------------

class Pasta(models.Model):
    id_pasta        = models.IntegerField(max_length=3, primary_key=True)
    pasta_pai       = models.ForeignKey('self', null= False)
    nome            = models.CharField(max_length=30)
    diretorio       = models.CharField(max_length=200)
    
    class Meta:
        db_table= 'tb_pasta'
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if len(Pasta.objects.using(Controle().getBanco()).order_by('-id_pasta')) > 0:   
            iUltimoRegistro = Pasta.objects.using(Controle().getBanco()).order_by('-id_pasta')[0] 
            self.id_pasta= iUltimoRegistro.pk + 1
        else:
            self.id_pasta= 1
        super(Pasta, self).save(using=Controle().getBanco())

#-----------------------------GRUPO----------------------------------------

class Grupo(models.Model):
    id_grupo        = models.IntegerField(max_length=3, primary_key=True)
    nome            = models.CharField(max_length=100)
    descricacao     = models.CharField(max_length=100)
    
    class Meta:
        db_table= 'tb_grupo'
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if len(Grupo.objects.using(Controle().getBanco()).order_by('-id_grupo')) > 0:   
            iUltimoRegistro = Grupo.objects.using(Controle().getBanco()).order_by('-id_grupo')[0] 
            self.id_grupo= iUltimoRegistro.pk + 1
        else:
            self.id_grupo= 1
        super(Grupo, self).save(using=Controle().getBanco())
        
class Grupo_Pasta(models.Model):
    id_grupo_pasta          = models.IntegerField(max_length=3, primary_key=True)
    grupo                   = models.ForeignKey(Grupo, null= False)
    pasta                   = models.ForeignKey(Pasta, null= False)
    
    class Meta:
        db_table= 'tb_grupo_pasta'
    
    def __unicode__(self):
        return self.id_grupo_pasta
    
    def save(self):  
        if len(Grupo_Pasta.objects.using(Controle().getBanco()).order_by('-id_grupo_pasta')) > 0:   
            iUltimoRegistro = Grupo_Pasta.objects.using(Controle().getBanco()).order_by('-id_grupo_pasta')[0] 
            self.id_grupo_pasta= iUltimoRegistro.pk + 1
        else:
            self.id_grupo_pasta= 1
        super(Grupo_Pasta, self).save(using=Controle().getBanco())
        
#-----------------------------FUNCAO----------------------------------------

class Funcao(models.Model):
    id_funcao       = models.IntegerField(max_length=3, primary_key=True)
    nome            = models.CharField(max_length=100)
    descricacao     = models.CharField(max_length=100)
    
    class Meta:
        db_table= 'tb_funcao'
    
    def __unicode__(self):
        return self.nome
    
    def save(self):  
        if len(Funcao.objects.using(Controle().getBanco()).order_by('-id_funcao')) > 0:   
            iUltimoRegistro = Funcao.objects.using(Controle().getBanco()).order_by('-id_funcao')[0] 
            self.id_funcao= iUltimoRegistro.pk + 1
        else:
            self.id_funcao= 1
        super(Funcao, self).save(using=Controle().getBanco())

class Funcao_Grupo(models.Model):
    id_funcao_grupo         = models.IntegerField(max_length=3, primary_key=True)
    funcao                  = models.ForeignKey(Funcao, null= False)
    grupo                   = models.ForeignKey(Grupo, null= False)
    
    class Meta:
        db_table= 'tb_funcao_grupo'
    
    def __unicode__(self):
        return self.id_funcao_grupo
    
    def save(self):  
        if len(Funcao_Grupo.objects.using(Controle().getBanco()).order_by('-id_funcao_grupo')) > 0:   
            iUltimoRegistro = Funcao_Grupo.objects.using(Controle().getBanco()).order_by('-id_funcao_grupo')[0] 
            self.id_funcao_grupo= iUltimoRegistro.pk + 1
        else:
            self.id_funcao_grupo= 1
        super(Funcao_Grupo, self).save(using=Controle().getBanco())

#-----------------------------IPs_PERMETIDOS----------------------------------------

class Firewall(models.Model):
    id_firewall     = models.IntegerField(max_length=3, primary_key=True)
    ip              = models.CharField(max_length=20)
    descricacao     = models.CharField(max_length=100)
    
    class Meta:
        db_table= 'tb_firewall'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Firewall.objects.using(Controle().getBanco()).order_by('-id_firewall')) > 0:   
            iUltimoRegistro = Firewall.objects.using(Controle().getBanco()).order_by('-id_firewall')[0] 
            self.id_firewall= iUltimoRegistro.pk + 1
        else:
            self.id_firewall= 1
        super(Firewall, self).save(using=Controle().getBanco())

class Firewall_Grupo(models.Model):
    id_firewall_grupo       = models.IntegerField(max_length=3, primary_key=True)
    firewall                = models.ForeignKey(Funcao, null= False)
    grupo                   = models.ForeignKey(Grupo, null= False)
    
    class Meta:
        db_table= 'tb_firewall_grupo'
    
    def __unicode__(self):
        return self.id_firewall_grupo
    
    def save(self):  
        if len(Firewall_Grupo.objects.using(Controle().getBanco()).order_by('-id_firewall_grupo')) > 0:   
            iUltimoRegistro = Firewall_Grupo.objects.using(Controle().getBanco()).order_by('-id_firewall_grupo')[0] 
            self.id_firewall_grupo= iUltimoRegistro.pk + 1
        else:
            self.id_firewall_grupo= 1
        super(Firewall_Grupo, self).save(using=Controle().getBanco())
