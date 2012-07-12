'''
Created on Jan 30, 2012

@author: spengler
'''

from django.conf.urls.defaults import * 

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     #url('^login/$', 'sign_up', name='sign_up'),
    (r'^login/$', 'django.contrib.auth.views.login',
       {'template_name': 'login.html'}, 'login'),
                    
    (r'^logout/$', 'django.contrib.auth.views.logout',
       {'template_name': 'logout.html'}, 'logout'),

    (r'^login_error/$', 'django.contrib.auth.views.login',
       {'template_name': 'login_error.html'}, 'login_error'),
)

