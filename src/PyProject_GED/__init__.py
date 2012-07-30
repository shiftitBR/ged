import controle
from django.conf import settings
from django.contrib.auth.models import User

oControle= controle.Controle()

if not oControle.inicializaAplicacao():
    print 'Problemas ao inicilizar a aplicacao!'

User._meta.get_field_by_name('email')[0]._unique = True 