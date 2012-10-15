from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('servidor.views',
                      url('^importar_lote/$', 'importar_lote',
                            {'vTitulo': trans(u'importar_lote')}, name='importar_lote'),
                      
                      )