'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models
from PyProject_GED              import oControle

from autenticacao.models        import Empresa #@UnresolvedImport
from autenticacao.models        import Usuario #@UnresolvedImport
from seguranca.models           import Pasta #@UnresolvedImport
from multiuploader.models       import MultiuploaderImage #@UnresolvedImport

#-----------------------------DOCUMENTO----------------------------------------

class Tipo_de_Documento(models.Model):
    id_tipo_documento       = models.IntegerField(max_length=3, primary_key=True)
    descricao               = models.CharField(max_length=30)
    eh_nativo               = models.BooleanField(null= False)
    empresa                 = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_tipo_de_documento'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Tipo_de_Documento.objects.order_by('-id_tipo_documento')) > 0:   
            iUltimoRegistro = Tipo_de_Documento.objects.order_by('-id_tipo_documento')[0] 
            self.id_tipo_documento= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_documento= 1
        super(Tipo_de_Documento, self).save()

class Documento(models.Model):
    id_documento    = models.IntegerField(max_length=10, primary_key=True, blank=True)
    tipo_documento  = models.ForeignKey(Tipo_de_Documento, null= False)
    usr_responsavel = models.ForeignKey(Usuario, null= False)
    pasta           = models.ForeignKey(Pasta, null= False)
    assunto         = models.CharField(max_length=100, null= False)
    versao_atual    = models.IntegerField(max_length=3, null= False)
    data_validade   = models.DateTimeField(null= True)
    data_descarte   = models.DateTimeField(null= True)
    eh_publico      = models.BooleanField(null= False)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_documento'
    
    def __unicode__(self):
        return self.assunto
    
    def save(self): 
        if self.id_documento == '' or self.id_documento== None:
            if len(Documento.objects.order_by('-id_documento')) > 0:   
                iUltimoRegistro = Documento.objects.order_by('-id_documento')[0] 
                self.id_documento= iUltimoRegistro.pk + 1
            else:
                self.id_documento= 1
        super(Documento, self).save()   

#-----------------------------VERSAO----------------------------------------
        
class Estado_da_Versao(models.Model):
    id_estado_da_versao = models.IntegerField(max_length=3, primary_key=True)
    descricao           = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_estado_da_versao'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Estado_da_Versao.objects.order_by('-id_estado_da_versao')) > 0:   
            iUltimoRegistro = Estado_da_Versao.objects.order_by('-id_estado_da_versao')[0] 
            self.id_estado_da_versao= iUltimoRegistro.pk + 1
        else:
            self.id_estado_da_versao= 1
        super(Estado_da_Versao, self).save(using=oControle.getBanco())
        
class Versao(models.Model):
    id_versao       = models.IntegerField(max_length=10, primary_key=True, blank=True)
    documento       = models.ForeignKey(Documento, null= False)
    usr_criador     = models.ForeignKey(Usuario, null= False)
    estado          = models.ForeignKey(Estado_da_Versao, null= False)
    versao          = models.IntegerField(max_length=3, null= False)
    dsc_modificacao = models.CharField(max_length=200, null= True)
    upload          = models.ForeignKey(MultiuploaderImage, null= False)
    protocolo       = models.CharField(max_length=20, null=True)
    data_criacao    = models.DateTimeField(null= False)
    eh_assinado     = models.BooleanField(null= False)
    
    class Meta:
        db_table= 'tb_versao'
    
    def __unicode__(self):
        return str(self.id_versao)
    
    def save(self): 
        if self.id_versao == '' or self.id_versao == None:
            if len(Versao.objects.order_by('-id_versao')) > 0:   
                iUltimoRegistro = Versao.objects.order_by('-id_versao')[0] 
                self.id_versao= iUltimoRegistro.pk + 1
            else:
                self.id_versao= 1
        super(Versao, self).save()   
        

