from django.conf.urls.defaults      import patterns, include, url
from django.conf                    import settings
from django.contrib                 import admin
from autenticacao.admin_empresas    import othersite, othersite2

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_empresa01/', include(othersite.urls)),
    url(r'^admin_empresa02/', include(othersite2.urls)),
    (r'^media/(.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^', include('flatpages.urls')),
    (r'^', include('documento.urls')),
    (r'^', include('autenticacao.urls')),
    (r'^', include('historico.urls')),
    (r'^', include('indice.urls')),
    (r'^', include('qualidade.urls')),
    (r'^', include('seguranca.urls')),
    url(r'', include('multiuploader.urls')),
)

    