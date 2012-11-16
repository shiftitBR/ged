from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('assinatura.views',
                        url('^assinar/(?P<vIDVersao>\d+)/$', 'assinar',
                            {'vTitulo': trans(u'assinar')}, name='assinar'), 
                      
                      )