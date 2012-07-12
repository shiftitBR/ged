'''
Created on Jul 11, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models
from django.contrib.auth.models import User

import constantes #@UnresolvedImport

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
    banco           = models.CharField(max_length=20, null= False, blank=True)
    eh_ativo        = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_empresa'
    
    def __unicode__(self):
        return "%s - %s" % (str(self.id_empresa), self.nome)
    
    def save(self, vBanco=constantes.cntConfiguracaoBancoPadrao):  
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>1'
        print vBanco
        if self.id_empresa == None: 
            if len(Empresa.objects.using(vBanco).order_by('-id_empresa')) > 0:   
                iUltimoRegistro = Empresa.objects.using(vBanco).order_by('-id_empresa')[0] 
                self.id_empresa= iUltimoRegistro.pk + 1
            else:
                self.id_empresa= 1
        super(Empresa, self).save(using=vBanco)

#---------------------------USUARIO---------------------------------------

class Tipo_de_Usuario(models.Model):
    id_tipo_usuario     = models.IntegerField(max_length=2, primary_key=True)
    descricao           = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_tipo_de_usuario'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self, vBanco):  
        if len(Tipo_de_Usuario.objects.using(vBanco).order_by('-id_tipo_usuario')) > 0:   
            iUltimoRegistro = Tipo_de_Usuario.objects.using(vBanco).order_by('-id_tipo_usuario')[0] 
            self.id_tipo_usuario= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_usuario= 1
        super(Tipo_de_Usuario, self).save(using=vBanco)

class Usuario(User):
    empresa         = models.ForeignKey(Empresa, null= False)
    tipo_usuario    = models.ForeignKey(Tipo_de_Usuario, null= False)
    eh_ativo        = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_usuario'
    
    def __unicode__(self):
        return self.username
    
    def save(self, vBanco): 
        if self.username == '':
            if len(User.objects.using(vBanco).order_by('-id')) > 0:   
                iUltimoRegistro = User.objects.using(vBanco).order_by('-id')[0] 
                self.username= "%03d-%06d" % (int(self.empresa.pk), int(iUltimoRegistro.pk) + 1)
            else:
                self.username= "%03d-%06d" % (int(self.empresa.pk), 1)
        super(Usuario, self).save(using=vBanco)    
        
