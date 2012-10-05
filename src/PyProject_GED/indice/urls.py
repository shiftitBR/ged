from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('indice.views',
                      url('^busca/(?P<vIDTipoBusca>\d+)/$', 'busca',
                          {'vTitulo': trans(u'busca')}, name='busca'),
                      url('^publico/(?P<vIDEmpresa>\d+)/$', 'publico',
                          {'vTitulo': trans(u'publico')}, name='publico'),
                      
                      )