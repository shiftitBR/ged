from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('historico.views',
                      url('^historico/$', 'historico',
                          {'vTitulo': trans(u'historico')}, name='historico'),
                      
                      )