'''
Created on Jan 30, 2012

@author: spengler
'''

from django.contrib.auth.models import User, check_password

from controle import Controle #@UnresolvedImport
from models import Usuario

import constantes #@UnresolvedImport

class EmailAuthBackend(object):
    """
    Email Authentication Backend
    
    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    oControle= Controle()
    
    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                iListaUsuario= Usuario.objects.filter(pk= user.pk)
                iUsuario= iListaUsuario[0]
                if len(iListaUsuario) > 0:
                    self.oControle.setBanco(iUsuario.empresa.banco)
                    self.oControle.setPasta(iUsuario.empresa.pasta_raiz)
                else:
                    self.oControle.setBanco(constantes.cntConfiguracaoBancoPadrao)
                return user
        except User.DoesNotExist:
            return None 

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None