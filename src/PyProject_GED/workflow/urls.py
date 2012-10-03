from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('workflow.views',
                      url('^encaminhar/(?P<vIDVersao>\d+)/$', 'encaminhar',
                            {'vTitulo': trans(u'encaminhar')}, name='encaminhar'),
                      url('^acompanhamento/$', 'acompanhamento',
                            {'vTitulo': trans(u'acompanhamento')}, name='acompanhamento'),
                      url('^tipo_pendencia/(?P<vIDVersao>\d+)/$', 'tipo_pendencia',
                            {'vTitulo': trans(u'tipo_pendencia')}, name='tipo_pendencia'),
                      url('^quantidade_pendencias/$', 'obtemQuantidadeDePendencias',
                            {'vTitulo': trans(u'obtemQuantidadeDePendencias')}, name='obtemQuantidadeDePendencias'),
                      )