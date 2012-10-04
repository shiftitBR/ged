# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2012

@author: Shift IT | wwww.shiftit.com.br
'''
from django.db                  import models
from documento.models           import Versao #@UnresolvedImport
from autenticacao.models        import Empresa #@UnresolvedImport

import logging
from PyProject_GED.seguranca.models import Pasta

#-----------------------------INDICE----------------------------------------

class Tipo_de_Indice(models.Model):
    id_tipo_indice          = models.IntegerField(max_length=3, primary_key=True, blank=True)
    descricao               = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_tipo_de_indice'
        verbose_name = 'Tipo de Índice'
        verbose_name_plural = 'Tipos de Índice'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if self.id_tipo_indice == None:
            if len(Tipo_de_Indice.objects.order_by('-id_tipo_indice')) > 0:   
                iUltimoRegistro = Tipo_de_Indice.objects.order_by('-id_tipo_indice')[0] 
                self.id_tipo_indice= iUltimoRegistro.pk + 1
            else:
                self.id_tipo_indice= 1
        super(Tipo_de_Indice, self).save()
    
    def criaTipoIndice(self, vDescricao):
        try:
            iTipoDeIndice= Tipo_de_Indice()
            iTipoDeIndice.descricao= vDescricao
            iTipoDeIndice.save()
            return iTipoDeIndice
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os tipos de Indice: ' + str(e))
            return False

class Indice(models.Model):
    id_indice       = models.IntegerField(max_length=3, primary_key=True, blank=True)
    descricao       = models.CharField(max_length=30)
    tipo_indice     = models.ForeignKey(Tipo_de_Indice, null= False)
    empresa         = models.ForeignKey(Empresa, null= False)
    
    class Meta:
        db_table= 'tb_indice'
        verbose_name = 'Índice'
        verbose_name_plural = 'Índices'
    
    def __unicode__(self):
        return self.descricao
    
    def save(self):  
        if self.id_indice == None:
            if len(Indice.objects.order_by('-id_indice')) > 0:   
                iUltimoRegistro = Indice.objects.order_by('-id_indice')[0] 
                self.id_indice= iUltimoRegistro.pk + 1
            else:
                self.id_indice= 1
        super(Indice, self).save()
    
    def obtemListaIndices(self, vIDEmpresa):
        try:
            iListaIndices = Indice.objects.filter(empresa= vIDEmpresa)
            return iListaIndices
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de indices: ' + str(e))
            return False

class Indice_Pasta(models.Model):
    id_indice_pasta = models.IntegerField(max_length=3, primary_key=True)
    indice          = models.ForeignKey(Indice, null= False)
    pasta           = models.ForeignKey(Pasta, null= False)
    
    class Meta:
        db_table= 'tb_indice_pasta'
        verbose_name = 'Associar Índice a Pasta'
        verbose_name_plural = 'Associar Índices a Pasta'
    
    def __unicode__(self):
        return str(self.id_indice_pasta)
    
    def save(self):  
        if self.id_indice_pasta == None:
            if len(Indice_Pasta.objects.order_by('-id_indice_pasta')) > 0:   
                iUltimoRegistro = Indice_Pasta.objects.order_by('-id_indice_pasta')[0] 
                self.id_indice_pasta= iUltimoRegistro.pk + 1
            else:
                self.id_indice_pasta= 1
        super(Indice_Pasta, self).save()
    
    def criaIndice_Pasta(self, vIndice, vPasta, vIndiceID=None, vPastaID=None):
        try:
            if vPastaID != None:
                iPasta= Pasta.objects.filter(id_pasta= int(vPastaID))[0]
            else:
                iPasta= vPasta
            if vIndiceID != None:
                iIndice= Indice.objects.filter(id_indice= int(vIndiceID))[0]
            else:
                iIndice= vIndice
            iIndice_Pasta       = Indice_Pasta()
            iIndice_Pasta.indice= iIndice
            iIndice_Pasta.pasta = iPasta
            iIndice_Pasta.save()
            return iIndice_Pasta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar Grupo_Indice: ' + str(e))
            return False
        
    def excluiIndicesDaPasta(self, vPasta, vPastaID=None):
        try:
            if vPastaID != None:
                iPasta= Pasta.objects.filter(id_pasta= int(vPastaID))[0]
            else:
                iPasta= vPasta
            Indice_Pasta.objects.filter(pasta= iPasta).delete()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel excluir indices da pasta: ' + str(e))
            return False 
    
    def obtemIndicesDaPasta(self, vIDPasta):
        try:
            iListaIndicesPasta = Indice_Pasta.objects.filter(pasta__id_pasta= vIDPasta)
            iListaIndices= []
            for iIndicesPasta in iListaIndicesPasta:
                iListaIndices.append(iIndicesPasta.indice)
            return iListaIndices
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de indices da pasta: ' + str(e))
            return False
    
    def obtemListaDePastasSemIndice(self, vEmpresa=None):
        try:
            iListaPastas        = Pasta.objects.all()
            iListaIndicePasta   = Indice_Pasta.objects.all()
            if vEmpresa != None:
                iListaPasta         = iListaPastas.filter(empresa= vEmpresa)
                iListaIndicePasta   = iListaIndicePasta.filter(pasta__empresa= vEmpresa)
            iListaPastasSemIndice   = []
            iListaPastasComIndice   = []
            for iIndicePasta in iListaIndicePasta:
                iListaPastasComIndice.append(iIndicePasta.pasta)
            for iPasta in iListaPasta:
                if iPasta not in iListaPastasComIndice:
                    iListaPastasSemIndice.append(iPasta)
            return iListaPastasSemIndice
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter lista de pastas sem indice: ' + str(e))
            return False
    
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
        if self.id_indice_versao_valor == None:
            if len(Indice_Versao_Valor.objects.order_by('-id_indice_versao_valor')) > 0:   
                iUltimoRegistro = Indice_Versao_Valor.objects.order_by('-id_indice_versao_valor')[0] 
                self.id_indice_versao_valor= iUltimoRegistro.pk + 1
            else:
                self.id_indice_versao_valor= 1
        super(Indice_Versao_Valor, self).save()
    
    def salvaValorIndice(self, vValor, vIDIndice, vIDVersao):
        try:
            iIndice         = Indice.objects.filter(id_indice= vIDIndice)[0]
            iVersao         = Versao.objects.filter(id_versao= vIDVersao)[0]
            
            iIndice_Versao_Valor        = Indice_Versao_Valor()
            iIndice_Versao_Valor.indice = iIndice
            iIndice_Versao_Valor.versao = iVersao
            iIndice_Versao_Valor.valor  = vValor
            iIndice_Versao_Valor.save()
            return iVersao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar a Versao do Documento: ' + str(e))
            return False
    
    def obtemIDVersoesFiltradosPorIndice(self, vIDEmpresa, vIDIndice, vValor):
        try:
            iListaVersoesIndice= []
            iListaVersaoIndice= Indice_Versao_Valor.objects.filter(indice__empresa__id_empresa= vIDEmpresa)
            iListaVersaoIndice= iListaVersaoIndice.filter(indice__id_indice= vIDIndice)
            iListaVersaoIndice= iListaVersaoIndice.filter(valor__iexact= vValor)
            for i in range(len(iListaVersaoIndice)):
                iListaVersoesIndice.append(iListaVersaoIndice[i].versao.id_versao)
            return iListaVersoesIndice
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter IDs das Versoes: ' + str(e))
            return False