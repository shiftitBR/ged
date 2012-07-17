from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('documento.views',
                      url('^documentos/$', 'documentos',
                          {'vTitulo': trans(u'documentos')}, name='documentos'), 
                      url('^checkin/(?P<vIDVersao>\d+)/$', 'checkin',
                          {'vTitulo': trans(u'checkin')}, name='checkin'),
                      url('^checkout/(?P<vIDVersao>\d+)/$', 'checkout',
                          {'vTitulo': trans(u'checkout')}, name='checkout'),
                      url('^importar_documento/$', 'importar',
                          {'vTitulo': trans(u'importar')}, name='importar'),
                      url('^aprovar_documento/(?P<vIDVersao>\d+)/$', 'aprovar',
                          {'vTitulo': trans(u'aprovar')}, name='aprovar'),
                      url('^reprovar_documento/(?P<vIDVersao>\d+)/$', 'reprovar',
                          {'vTitulo': trans(u'reprovar')}, name='reprovar'),
                      url('^excluir_documento/(?P<vIDVersao>\d+)/$', 'excluir',
                          {'vTitulo': trans(u'excluir')}, name='excluir'),
                      url('^informacoes_documento/(?P<vIDVersao>\d+)/$', 'informacoes',
                          {'vTitulo': trans(u'informacoes')}, name='informacoes'),

                      )