# -*- coding: utf-8 -*-
from django.db                          import models
from django.db.models                   import get_model
import random

from django.conf                        import settings
from PyProject_GED                      import oControle
from django.utils.encoding              import smart_str, smart_unicode
import os
from threading import BoundedSemaphore, Thread

oListaUploads= []
oSemafaros= {}
iConexoesSimultaneas = 1
iSemafaroGeral = BoundedSemaphore(value=iConexoesSimultaneas)
print '>>>>>>>>>>>>>>>>>>>>cre'


try:
    storage = settings.MULTI_IMAGES_FOLDER+'/'
except AttributeError:
    storage = 'multiuploader_images/'

class MultiuploaderImage(models.Model):
    """Model for storing uploaded photos"""
    filename = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(max_length=500, upload_to=storage)
    key_data = models.CharField(max_length=90, unique=True, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def key_generate(self):
        """returns a string based unique key with length 80 chars"""
        while 1:
            key = str(random.getrandbits(256))
            try:
                MultiuploaderImage.objects.get(key=key)
            except:
                return key

    def __unicode__(self):
        return self.image.name

    def save(self, vIDPasta, vIDEmpresa):
        try:
            mPasta= get_model('seguranca', 'Pasta')()
            for field in self._meta.fields:
                if field.name == 'image':
                    field.upload_to = mPasta.obtemDiretorioUpload(vIDPasta, vIDEmpresa)
            super(MultiuploaderImage, self).save()
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel salvar - multiuploader: ' + str(e))
            return False

        
    def obtemImagePeloId(self, vIDImage):
        return MultiuploaderImage.objects.filter(id=vIDImage)[0]
    
    def limpaNomeImagem(self, vNomeImagem):
        try:
            iNomeImagem, iExtencao= os.path.splitext(str(vNomeImagem))
            iNomeLimpo= ''.join(e for e in iNomeImagem if e.isalnum())
            return u'%s%s' % (iNomeLimpo.lower(), iExtencao.lower())
        except:
            return False
    
    def limpaNomeImagemSuave(self, vNomeImagem):
        try:
            return vNomeImagem.replace('ª', 'a')
        except:
            return False
    
    def insereUploadDoUsuario(self, vIDUsuario, vIDUpload):
        try:
            oListaUploads.append((vIDUsuario, vIDUpload))
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel iserir upload na lista: ' + str(e))
            return False
    
    def obtemListaDeUploadsDoUsuario(self, vIDUsuario):
        try:
            iListaUploads= []
            iListaIndices=[]
            for i in range(len(oListaUploads)):
                if oListaUploads[i][0] == vIDUsuario:
                    iListaUploads.append(oListaUploads[i][1])
                    iListaIndices.append(i)
            iListaIndices.reverse()
            for iIndice in iListaIndices:
                oListaUploads.pop(iIndice)            
            return iListaUploads
        
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel iserir upload na lista: ' + str(e))
            return False
        
    def criaSemafaro(self, vIDUsuario):
        try:
            iConexoesSimultaneas = 1
            iSemafaro = BoundedSemaphore(value=iConexoesSimultaneas)
            oSemafaros[vIDUsuario]= iSemafaro
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel criar o semafaro: ' + str(e))
            return False

    def obtemSemaforo(self, vIDUsuario):
        try:
            iObteve= False
            while not iObteve:    
                try:
                    iSemafaroGeral.acquire()
                    iSemafaro = oSemafaros[vIDUsuario]
                    iObteve= True
                    iSemafaroGeral.release()
                except:
                    iObteve= False
            return iSemafaro
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel obter o semafaro: ' + str(e))
            return False