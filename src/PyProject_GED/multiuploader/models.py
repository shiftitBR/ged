# -*- coding: utf-8 -*-
from django.db                          import models
from django.db.models                   import get_model
import random

from django.conf                        import settings
from PyProject_GED                      import oControle
from PyProject_GED.autenticacao.models  import Usuario

import os
from django.db.models.aggregates import Max
import unicodedata
import string

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
    usuario= models.ForeignKey(Usuario, blank=True, null=True)
    grupo= models.IntegerField(max_length=10, blank=True, null=True)
    
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
            iNomeImagem, iExtencao = os.path.splitext(vNomeImagem)
            iNomeLimpo= ''.join(x for x in unicodedata.normalize('NFKD', iNomeImagem) if x in string.ascii_letters).lower()
            return u'%s%s' % (iNomeLimpo.lower(), iExtencao.lower())
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel limpar o nome do arquivo: ' + str(e))
            return False
    
    def obtemListaDeUploadsDoUsuario(self, vUser, vIDGrupo):
        try:
            iUsuario= Usuario().obtemUsuario(vUser)
            iListaUploads= MultiuploaderImage.objects.filter(usuario= iUsuario, grupo= vIDGrupo)
            return iListaUploads
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel obter lista de uploads: ' + str(e))
            return False
    
    def obtemGrupoDeUpload(self):
        try:
            iUltimoGrupo= MultiuploaderImage.objects.all().aggregate(Max('grupo'))['grupo__max']
            if iUltimoGrupo == None:
                iProximoGrupo= 1
            else:
                iProximoGrupo= iUltimoGrupo +1
            return iProximoGrupo
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel obter o grupo de upload: ' + str(e))
            return False
    

 