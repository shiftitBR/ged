from django.conf.urls.defaults      import patterns, include, url
from django.conf                    import settings
from django.contrib                 import admin

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
    (r'^', include('workflow.urls')),
    (r'^', include('envioemail.urls')),
    (r'^', include('scanner.urls')),
    (r'^', include('gerenciamento.urls')),
    url(r'', include('multiuploader.urls')),
)

    