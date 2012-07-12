import controle
from django.conf import settings

oControle= controle.Controle()

if not oControle.inicializaAplicacao():
    print 'Problemas ao inicilizar a aplicacao!'