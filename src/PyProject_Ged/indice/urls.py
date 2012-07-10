from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('indice.views',
                      url('^busca/$', 'busca',
                          {'vTitulo': trans(u'busca')}, name='busca'),
                      
                      )