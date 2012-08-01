from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('workflow.views',
                      url('^encaminhar/(?P<vIDVersao>\d+)/$', 'encaminhar',
                            {'vTitulo': trans(u'encaminhar')}, name='encaminhar'),
                      url('^acompanhamento/$', 'acompanhamento',
                            {'vTitulo': trans(u'acompanhamento')}, name='acompanhamento'),
                      )