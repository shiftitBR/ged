from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('flatpages.views',
                      url('^$', 'home',
                          {'vTitulo': trans(u'Home')}, name='home'), 
                      
                      )