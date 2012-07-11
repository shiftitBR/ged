from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('documento.views',
                      url('^documentos/$', 'documentos',
                          {'vTitulo': trans(u'documentos')}, name='documentos'), 
                      url('^checkin/$', 'checkin',
                          {'vTitulo': trans(u'checkin')}, name='checkin'),
                      url('^importar_documento/$', 'importar',
                          {'vTitulo': trans(u'importar')}, name='importar'),
                      url('^aprovar_documento/$', 'aprovar',
                          {'vTitulo': trans(u'aprovar')}, name='aprovar'),
                      url('^reprovar_documento/$', 'reprovar',
                          {'vTitulo': trans(u'reprovar')}, name='reprovar'),
                      url('^excluir_documento/$', 'excluir',
                          {'vTitulo': trans(u'excluir')}, name='excluir'),
                      url('^informacoes_documento/$', 'informacoes',
                          {'vTitulo': trans(u'informacoes')}, name='informacoes'),

                      )