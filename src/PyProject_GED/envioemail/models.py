'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models

from PyProject_GED.documento.models     import Documento
from PyProject_GED.autenticacao.models  import Usuario

import logging

#-----------------------------Publicacao----------------------------------------

class Publicacao(models.Model):
    id_publicacao   = models.IntegerField(max_length=10, primary_key=True, blank=True)
    usr_remetente   = models.ForeignKey(Usuario, null= False)
    
    class Meta:
        db_table= 'tb_publicacao'
    
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
            print str(e)
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
            print str(e)
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
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a Publicacao_Documento: ' + str(e))
            return False
        
    def obtemListaPublicacaoDocumento(self, vIDPublicacao):
        try:
            iListaPublicacaoDocumento = Publicacao_Documento.objects.filter(publicacao__id_publicacao= vIDPublicacao)
            return iListaPublicacaoDocumento
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obter a lista de publicacao_documento ' + str(e))
            return False
