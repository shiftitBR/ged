'''
Created on Jul 18, 2012

@author: Shift IT | wwww.shiftit.com.br
'''
from django.db                  import models
from controle                   import Controle #@UnresolvedImport

from documento.models           import Versao #@UnresolvedImport

#-----------------------------INDICE----------------------------------------

class Tipo_de_Indice(models.Model):
    id_tipo_indice          = models.IntegerField(max_length=3, primary_key=True)
    descricao               = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_tipo_de_indice'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Tipo_de_Indice.objects.using(Controle().getBanco()).order_by('-id_tipo_indice')) > 0:   
            iUltimoRegistro = Tipo_de_Indice.objects.using(Controle().getBanco()).order_by('-id_tipo_indice')[0] 
            self.id_tipo_indice= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_indice= 1
        super(Tipo_de_Indice, self).save(using=Controle().getBanco())

class Indice(models.Model):
    id_indice       = models.IntegerField(max_length=3, primary_key=True)
    descricao       = models.CharField(max_length=30)
    tipo_indice     = models.ForeignKey(Tipo_de_Indice, null= False)
    
    class Meta:
        db_table= 'tb_indice'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if len(Indice.objects.using(Controle().getBanco()).order_by('-id_indice')) > 0:   
            iUltimoRegistro = Indice.objects.using(Controle().getBanco()).order_by('-id_indice')[0] 
            self.id_indice= iUltimoRegistro.pk + 1
        else:
            self.id_indice= 1
        super(Indice, self).save(using=Controle().getBanco())

class Indice_Versao_Valor(models.Model):
    id_indice_versao_valor  = models.IntegerField(max_length=3, primary_key=True)
    indice                  = models.ForeignKey(Indice, null= False)
    versao                  = models.ForeignKey(Versao, null= False)
    valor                   = models.CharField(max_length=50)
    
    class Meta:
        db_table= 'tb_indice_versao_valor'
    
    def __unicode__(self):
        return self.id_indice_versao_valor
    
    def save(self):  
        if len(Indice_Versao_Valor.objects.using(Controle().getBanco()).order_by('-id_indice_versao_valor')) > 0:   
            iUltimoRegistro = Indice_Versao_Valor.objects.using(Controle().getBanco()).order_by('-id_indice_versao_valor')[0] 
            self.id_indice_versao_valor= iUltimoRegistro.pk + 1
        else:
            self.id_indice_versao_valor= 1
        super(Indice_Versao_Valor, self).save(using=Controle().getBanco())