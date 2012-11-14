from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('flatpages.views',
                      url('^$', 'home',
                          {'vTitulo': trans(u'Home')}, name='home'), 
                      url('^enderecos/$', 'enderecos',
                          {'vTitulo': trans(u'enderecos')}, name='enderecos'), 
                      url('^publicacao/(?P<vIDPublicacao>\d+)/$', 'publicacao',
                          {'vTitulo': trans(u'publicacao')}, name='publicacao'),
                      url('^sucesso/(?P<vAcao>\d+)/$', 'sucesso',
                          {'vTitulo': trans(u'sucesso')}, name='sucesso'),
                      url('^ajuda/$', 'ajuda',
                          {'vTitulo': trans(u'ajuda')}, name='ajuda'),
                      url('^download_importador/$', 'download_importador',
                          {'vTitulo': trans(u'download_importador')}, name='download_importador'),
                      )