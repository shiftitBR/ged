'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db import models

class Certificado(models.Model):
    arquivo = models.FileField(upload_to='documentos/certificados/')
    
    class Meta:
        db_table= 'tb_certificado'
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        
    def __unicode__(self):
        return str(self.arquivo)