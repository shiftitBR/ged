from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('gerenciamento.views',
                      url('^gerenciamento/$', 'gerenciamento',
                            {'vTitulo': trans(u'gerencianento')}, name='gerenciamento'),

                      )