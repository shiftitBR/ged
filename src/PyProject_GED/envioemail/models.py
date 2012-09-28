# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models

from PyProject_GED.documento.models     import Documento
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.envioemail.controle  import Controle as EmailControle

import logging

#-----------------------------Publicacao----------------------------------------

class Publicacao(models.Model):
    id_publicacao   = models.IntegerField(max_length=10, primary_key=True, blank=True)
    usr_remetente   = models.ForeignKey(Usuario, null= False)
    
    class Meta:
        db_table= 'tb_publicacao'
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'
    
    def __unicode__(self):
        return self.id_publicacao
    
    def save(self): 
        if self.id_publicacao == '' or self.id_publicacao== None:
            if len(Publicacao.objects.order_by('-id_publicacao')) > 0:   
                iUltimoRegistro = Publicacao.objects.order_by('-id_publicacao')[0] 
                self.id_publicacao= iUltimoRegistro.pk + 1
            else:
                self.id_publicacao= 1
        super(Publicacao, self).save()  
        
    def criarPublicacao(self, VRemente):
        try:
            iPublicacao                 = Publicacao()
            iPublicacao.usr_remetente   = VRemente
            iPublicacao.save()
            return iPublicacao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a Publicacao: ' + str(e))
            return False
        
    def obtemPublicacao(self, vIDPublicacao):
        try:
            iPublicacao = Publicacao.objects.filter(id_publicacao= vIDPublicacao)[0]
            return iPublicacao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a publicacao ' + str(e))
            return False
            
class Publicacao_Usuario(models.Model):
    id_publicacao_usuario = models.IntegerField(max_length=10, primary_key=True, blank=True)
    publicacao            = models.ForeignKey(Publicacao, null= False)
    usr_destinatario      = models.ForeignKey(Usuario, null= False)
    
    class Meta:
        db_table= 'tb_publicacao_usuario'
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'
    
    def __unicode__(self):
        return self.id_publicacao_usuario
    
    def save(self): 
        if self.id_publicacao_usuario == '' or self.id_publicacao_usuario== None:
            if len(Publicacao_Usuario.objects.order_by('-id_publicacao_usuario')) > 0:   
                iUltimoRegistro = Publicacao_Usuario.objects.order_by('-id_publicacao_usuario')[0] 
                self.id_publicacao_usuario= iUltimoRegistro.pk + 1
            else:
                self.id_publicacao_usuario= 1
        super(Publicacao_Usuario, self).save()  
        
    def criarPublicacaoUsuario(self, vPublicacao, vUsuario):
        try:
            iPublicacaoUsr                  = Publicacao_Usuario()
            iPublicacaoUsr.publicacao       = vPublicacao
            iPublicacaoUsr.usr_destinatario = vUsuario
            iPublicacaoUsr.save()
            return iPublicacaoUsr
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a Publicacao_Usuario: ' + str(e))
            return False
        
    def obtemListaPublicacaoUsuario(self, vIDPublicacao):
        try:
            iListaPublicacaoUsuario = Publicacao_Usuario.objects.filter(publicacao__id_publicacao= vIDPublicacao)
            return iListaPublicacaoUsuario
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de publicacao_usuario ' + str(e))
            return False
        
class Publicacao_Documento(models.Model):
    id_publicacao_documento = models.IntegerField(max_length=10, primary_key=True, blank=True)
    publicacao              = models.ForeignKey(Publicacao, null= False)
    documento               = models.ForeignKey(Documento, null= False)
    
    class Meta:
        db_table= 'tb_publicacao_documento'
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'
    
    def __unicode__(self):
        return self.id_publicacao
    
    def save(self): 
        if self.id_publicacao_documento == '' or self.id_publicacao_documento== None:
            if len(Publicacao_Documento.objects.order_by('-id_publicacao_documento')) > 0:   
                iUltimoRegistro = Publicacao_Documento.objects.order_by('-id_publicacao_documento')[0] 
                self.id_publicacao_documento= iUltimoRegistro.pk + 1
            else:
                self.id_publicacao_documento= 1
        super(Publicacao_Documento, self).save()  
        
    def criarPublicacaoDocumento(self, vPublicacao, vDocumento):
        try:
            iPublicacaoDoc                  = Publicacao_Documento()
            iPublicacaoDoc.publicacao       = vPublicacao
            iPublicacaoDoc.documento        = vDocumento
            iPublicacaoDoc.save()
            return iPublicacaoDoc
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a Publicacao_Documento: ' + str(e))
            return False
        
    def obtemListaPublicacaoDocumento(self, vIDPublicacao):
        try:
            iListaPublicacaoDocumento = Publicacao_Documento.objects.filter(publicacao__id_publicacao= vIDPublicacao)
            return iListaPublicacaoDocumento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de publicacao_documento ' + str(e))
            return False
        
#---------------------------------- EMAIL -------------------------------------------

class Tipo_de_Email(models.Model):
    id_tipo_email       = models.IntegerField(max_length=2, primary_key=True)
    descricao           = models.CharField(max_length=30)
    
    class Meta:
        db_table= 'tb_tipo_de_email'
    
    def save(self):  
        
        if len(Tipo_de_Email.objects.order_by('-id_tipo_email')) > 0:   
            iUltimoRegistro = Tipo_de_Email.objects.order_by('-id_tipo_email')[0] 
            self.id_tipo_email= iUltimoRegistro.pk + 1
        else:
            self.id_tipo_email= 1
        super(Tipo_de_Email, self).save()

class Email(models.Model):
    id_email        = models.IntegerField(max_length=2, primary_key=True, null= False)
    tipo_email      = models.ForeignKey(Tipo_de_Email, blank=False, unique=False)
    titulo          = models.CharField(max_length=100, null= True)
    mensagem        = models.CharField(max_length=4000, null= True)    
    
    class Meta:
        db_table= 'tb_email'
    
    def save(self):  
        if self.id_email == None: 
            if len(Email.objects.order_by('-tb_email')) > 0:   
                iUltimoRegistro = Email.objects.order_by('-tb_email')[0] 
                self.id_email= iUltimoRegistro.pk + 1
            else:
                self.id_email= 1
        super(Email, self).save()
        
    def enviaEmailPorTipo(self, vEmailRemetente, vEmailDestinatario, vTipoEmail):
        try:
            iEmail      = Email.objects.filter(tipo_email= vTipoEmail)[0]
            return EmailControle().enviarEmail(iEmail.titulo, iEmail.mensagem, vEmailDestinatario, vEmailRemetente)
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel envia Email Por Tipo: ' + str(e))
            return False
        
    def enviaEmail(self, vEmailRemetente, vEmailDestinatario, vTitulo, vMensagem):
        try:
            return EmailControle().enviarEmail(vTitulo, vMensagem, vEmailDestinatario, vEmailRemetente)
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel envia Email: ' + str(e))
            return False