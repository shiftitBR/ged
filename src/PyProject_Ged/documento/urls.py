from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('documento.views',
                      url('^documentos/$', 'documentos',
                          {'vTitulo': trans(u'socumentos')}, name='documentos'), 

                      )