'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from PyProject_GED.documento.models     import Documento
from PyProject_GED.autenticacao.models  import Empresa

import logging
        
#-----------------------------NORMA----------------------------------------

class Tipo_de_Norma(models.Model):
    id_tipo_norma       = models.IntegerField(max_length=3, primary_key=True)
    descricao           = models.CharField(max_length=50)
    empresa             = models.ForeignKey(Empresa, null= False)

    class Meta:
        db_table= 'tb_tipo_de_norma'
        verbose_name = 'Tipo de Norma'
        verbose_name_plural = 'Tipos de Norma'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if self.id_tipo_norma == '' or self.id_tipo_norma== None: 
            if len(Tipo_de_Norma.objects.order_by('-id_tipo_norma')) > 0:   
                iUltimoRegistro = Tipo_de_Norma.objects.order_by('-id_tipo_norma')[0] 
                self.id_tipo_norma= iUltimoRegistro.pk + 1
            else:
                self.id_tipo_norma= 1
        super(Tipo_de_Norma, self).save()

class Norma(models.Model):
    id_norma        = models.IntegerField(max_length=3, primary_key=True)
    descricao       = models.CharField(max_length=200)
    numero          = models.CharField(max_length=50)
    tipo_norma      = models.ForeignKey(Tipo_de_Norma, null= False)
    norma_pai       = models.ForeignKey('self', null=True, blank= True)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_norma'
        verbose_name = 'Norma'
        verbose_name_plural = 'Normas'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self): 
        if self.id_norma == '' or self.id_norma== None: 
            if len(Norma.objects.order_by('-id_norma')) > 0:   
                iUltimoRegistro = Norma.objects.order_by('-id_norma')[0] 
                self.id_norma= iUltimoRegistro.pk + 1
            else:
                self.id_norma= 1
        super(Norma, self).save()
        
    def criaNorma(self, vEmpresa, vDescricao, vNumero, vTipoNorma, vNormaPai=None):
        try:
            iNorma= Norma()
            iNorma.tipo_norma   = vTipoNorma
            iNorma.empresa      = vEmpresa
            iNorma.descricao    = vDescricao
            iNorma.norma_pai    = vNormaPai
            iNorma.save()
            return iNorma
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar normas: ' + str(e))
            return False
        
    def obtemNorma(self, vIDNorma):
        try:
            iNorma = Norma.objects.filter(id_norma= vIDNorma)[0]
            return iNorma
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar normas: ' + str(e))
            return False

class Norma_Documento(models.Model):
    id_norma_documento      = models.IntegerField(max_length=3, primary_key=True)
    norma                   = models.ForeignKey(Norma, null= False)
    documento               = models.ForeignKey(Documento, null= False)
    
    
    class Meta:
        db_table= 'tb_norma_documento'
    
    def __unicode__(self):
        return str(self.id_norma_documento)
    
    def save(self):  
        if self.id_norma_documento == '' or self.id_norma_documento== None: 
            if len(Norma_Documento.objects.order_by('-id_norma_documento')) > 0:   
                iUltimoRegistro = Norma_Documento.objects.order_by('-id_norma_documento')[0] 
                self.id_norma_documento= iUltimoRegistro.pk + 1
            else:
                self.id_norma_documento= 1
        super(Norma_Documento, self).save()
        
    def criaNorma_Documento(self, vNorma, vDocumento):
        try:
            iNorma_Documento            = Norma_Documento()
            iNorma_Documento.norma      = vNorma
            iNorma_Documento.documento  = vDocumento
            iNorma_Documento.save()
            return iNorma_Documento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Norma_Documento: ' + str(e))
            return False
    
    def obtemDocumentosPelaNorma(self, vNorma):
        try:
            iListaNormaDocumentos= Norma_Documento.objects.filter(norma= vNorma)
            iListaDocumentos= []
            for iDocumentoNorma in iListaNormaDocumentos:
                iListaDocumentos.append(iDocumentoNorma.documento)
            return iListaDocumentos
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter Documentos pela Norma: ' + str(e))
            return False
        