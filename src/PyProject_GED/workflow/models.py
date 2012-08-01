'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                          import models
from autenticacao.models                import Usuario #@UnresolvedImport
from documento.models                   import Versao #@UnresolvedImport

import logging
import datetime

#-----------------------------Pendencia----------------------------------------

class Pendencia(models.Model):
    id_pendencia    = models.IntegerField(max_length=3, primary_key=True)
    usr_remetente   = models.ForeignKey(Usuario, blank=True, unique=False, verbose_name='user', related_name="usr_remetente")
    usr_destinatario= models.ForeignKey(Usuario, blank=True, unique=False, verbose_name='user', related_name="usr_destinatario")
    versao          = models.ForeignKey(Versao, null= False)
    data            = models.CharField(max_length=100, null= False)
    descricao       = models.CharField(max_length=200, null= False)
    feedback        = models.CharField(max_length=200, null= True)
    
    class Meta:
        db_table= 'tb_pendencia'
    
    def __unicode__(self):
        return self.id_pendencia
    
    def save(self):  
        if len(Pendencia.objects.order_by('-id_pendencia')) > 0:   
            iUltimoRegistro = Pendencia.objects.order_by('-id_pendencia')[0] 
            self.id_pendencia= iUltimoRegistro.pk + 1
        else:
            self.id_pendencia= 1
        super(Pendencia, self).save()
    
    def criaPendencia(self, vRemetente, vDestinatario, vVersao, vDescricao, vData=str(datetime.datetime.today())[:19]):
        try:
            iPendencia= Pendencia()
            iPendencia.usr_remetente    = vRemetente
            iPendencia.usr_destinatario = vDestinatario
            iPendencia.versao           = vVersao   
            iPendencia.data             = vData    
            iPendencia.descricao        = vDescricao
            iPendencia.save()
            return iPendencia
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a pendencia: ' + str(e))
            return False
        
    def obtemListaPendenciasRemetente(self, vRemetente):
        try:
            return True
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaPendenciasRemetente: ' + str(e))
            return False
        
    def obtemListaPendenciasDestinatario(self, vDestinatario):
        try:
            return True
        except Exception, e:
            print str(e)
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel obtemListaPendenciasDestinatario: ' + str(e))
            return False
