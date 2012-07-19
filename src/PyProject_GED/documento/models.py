'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models
from PyProject_GED              import oControle

from autenticacao.models        import Usuario #@UnresolvedImport
from seguranca.models           import Pasta #@UnresolvedImport

#-----------------------------DOCUMENTO----------------------------------------

class Tipo_de_Documento(models.Model):
    id_tipo_documento       = models.IntegerField(max_length=3, primary_key=True)
    descricao               = models.CharField(max_length=30)
    eh_nativo               = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_tipo_de_documento'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Tipo_de_Documento.objects.using(oControle.getBanco()).order_by('-id_tipo_documento')) > 0:   
            iUltimoRegistro = Tipo_de_Documento.objects.using(oControle.getBanco()).order_by('-id_tipo_documento')[0] 
            self.id_tipo_documento= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_documento= 1
        super(Tipo_de_Documento, self).save(using=oControle.getBanco())

class Documento(models.Model):
    id_documento    = models.IntegerField(max_length=10, primary_key=True)
    tipo_documento  = models.ForeignKey(Tipo_de_Documento, null= False)
    usr_responsavel = models.ForeignKey(Usuario, null= False)
    pasta           = models.ForeignKey(Pasta, null= False)
    assunto         = models.CharField(max_length=100, null= False)
    versao_atual    = models.IntegerField(max_length=3, null= False)
    data_validade   = models.DateTimeField(null= False)
    data_descarte   = models.DateTimeField(null= False)
    eh_pulbico      = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_documento'
    
    def __unicode__(self):
        return self.assunto
    
    def save(self): 
        if self.id_documento == '':
            if len(Documento.objects.using(oControle.getBanco()).order_by('-id_documento')) > 0:   
                iUltimoRegistro = Documento.objects.using(oControle.getBanco()).order_by('-id_documento')[0] 
                self.id_documento= iUltimoRegistro.pk + 1
            else:
                self.id_documento= 1
        super(Documento, self).save(using=oControle.getBanco())   

#-----------------------------VERSAO----------------------------------------
        
class Estado_da_Versao(models.Model):
    id_estado_da_versao = models.IntegerField(max_length=3, primary_key=True)
    descricao           = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_estado_da_versao'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Estado_da_Versao.objects.using(oControle.getBanco()).order_by('-id_estado_da_versao')) > 0:   
            iUltimoRegistro = Estado_da_Versao.objects.using(oControle.getBanco()).order_by('-id_estado_da_versao')[0] 
            self.id_estado_da_versao= iUltimoRegistro.pk + 1
        else:
            self.id_estado_da_versao= 1
        super(Estado_da_Versao, self).save(using=oControle.getBanco())
        
class Versao(models.Model):
    id_versao       = models.IntegerField(max_length=10, primary_key=True)
    documento       = models.ForeignKey(Documento, null= False)
    usr_criador     = models.ForeignKey(Usuario, null= False)
    estado          = models.ForeignKey(Estado_da_Versao, null= False)
    versao          = models.IntegerField(max_length=3, null= False)
    dsc_modificacao = models.CharField(max_length=200, null= False)
    arquivo         = models.CharField(max_length=200, null= False)
    protocolo       = models.CharField(max_length=20)
    data_criacao    = models.DateTimeField(null= False)
    eh_assinado     = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_versao'
    
    def __unicode__(self):
        return self.id_versao
    
    def save(self): 
        if self.id_versao == '':
            if len(Versao.objects.using(oControle.getBanco()).order_by('-id_versao')) > 0:   
                iUltimoRegistro = Versao.objects.using(oControle.getBanco()).order_by('-id_versao')[0] 
                self.id_versao= iUltimoRegistro.pk + 1
            else:
                self.id_versao= 1
        super(Versao, self).save(using=oControle.getBanco())   
        

