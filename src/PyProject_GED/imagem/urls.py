from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('imagem.views',
                      url('^tipo_exportar/(?P<vIDVersao>\d+)/$', 'tipo_exportar',
                           {'vTitulo': trans(u'tipo_exportar')}, name='tipo_exportar'),
                      url('^negativar_imagem/$', 'negativar_imagem',
                           {'vTitulo': trans(u'negativar_imagem')}, name='negativar_imagem'),
                      url('^rotacionar_imagem/(?P<vLado>\d+)/$', 'rotacionar_imagem',
                           {'vTitulo': trans(u'rotacionar_imagem')}, name='rotacionar_imagem'),
                      )