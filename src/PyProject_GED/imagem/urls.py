from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('imagem.views',
                      url('^tipo_exportar/(?P<vIDVersao>\d+)/$', 'tipo_exportar',
                           {'vTitulo': trans(u'tipo_exportar')}, name='tipo_exportar'),
                      )