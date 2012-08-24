from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('scanner.views',
                        url('^importar_scanner/$', 'importar',
                            {'vTitulo': trans(u'importar')}, name='importar'),
                      )