from django.db                          import models
from django.db.models                   import get_model
import random

from django.conf import settings
try:
    storage = settings.MULTI_IMAGES_FOLDER+'/'
except AttributeError:
    storage = 'multiuploader_images/'

class MultiuploaderImage(models.Model):
    """Model for storing uploaded photos"""
    filename = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(max_length=300, upload_to=storage)
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

    def save(self, vIDPasta):
        mPasta= get_model('seguranca', 'Pasta')()
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = mPasta.obtemDiretorioUpload(vIDPasta)
        super(MultiuploaderImage, self).save()

