from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('relatorios.views',
                      url('^relatorios/$', 'relatorios',
                           {'vTitulo': trans(u'relatorios')}, name='relatorios'),
                      url('^estado_usuarios/$', 'estado_usuarios',
                           {'vTitulo': trans(u'estado_usuarios')}, name='estado_usuarios'),
                      url('^ultimos_acessos/$', 'ultimos_acessos',
                           {'vTitulo': trans(u'ultimos_acessos')}, name='ultimos_acessos'),
                      )