'''
Created on Jan 30, 2012

@author: spengler
'''

from django.conf.urls.defaults import * 
from django.utils.translation   import ugettext_lazy as trans

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('autenticacao.views',
     #url('^login/$', 'sign_up', name='sign_up'),
    url('^login/$', 'login', {'vTitulo': trans(u'login')}, name='login'),
    
    url('^logout/$', 'logout', {'vTitulo': trans(u'logout')}, name='logout'),
    
    url('^login_error/(?P<vTipoErro>\d+)/$', 'login_error', {'vTitulo': trans(u'login_error')}, name='login_error'),

)

