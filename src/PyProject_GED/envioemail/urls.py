from django.conf.urls.defaults  import *
from django.utils.translation   import ugettext_lazy as trans

urlpatterns= patterns('envioemail.views',
                        url('^email/$', 'email',
                          {'vTitulo': trans(u'email')}, name='email'),
                        url('^publicar/$', 'publicar',
                          {'vTitulo': trans(u'publicar')}, name='publicar'),
                      
                      )