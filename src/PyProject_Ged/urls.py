from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^', include('flatpages.urls')),
    (r'^', include('documento.urls')),
    (r'^', include('autenticacao.urls')),
    (r'^', include('historico.urls')),
    (r'^', include('indice.urls')),
    (r'^', include('qualidade.urls')),
    (r'^', include('seguranca.urls')),
)

    