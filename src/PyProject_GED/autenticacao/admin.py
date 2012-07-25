'''
Created on Jan 17, 2012

@author: spengler
'''

from django.contrib                 import admin
from django.contrib.auth.admin      import UserAdmin 

from models                         import Empresa
from models                         import Tipo_de_Usuario
from models                         import Usuario
from multiAdmin                     import MultiDBModelAdmin #@UnresolvedImport
from django.contrib.admin.options   import ModelAdmin


class AdminEmpresa(MultiDBModelAdmin): 
    list_display    = ('id_empresa', 'nome', 'cnpj', 'cep', 'rua', 'numero', 'complemento', 'bairro', 
                       'cidade', 'uf', 'eh_ativo')
    search_fields   = ('id_empresa', 'nome', 'cnpj', 'eh_ativo')
    list_filter     = ('id_empresa', 'nome', 'cnpj', 'eh_ativo')
    
class AdminTipo_de_Usuario(MultiDBModelAdmin): 
    list_display    = ('id_tipo_usuario', 'descricao')
    search_fields   = ('id_tipo_usuario',)
    list_filter     = ('id_tipo_usuario',)

class AdminUsuario(MultiDBModelAdmin): 
    list_display    = UserAdmin.list_display + ('empresa', 'tipo_usuario', 'eh_ativo')
    search_fields   = UserAdmin.search_fields
    list_filter     = UserAdmin.list_filter
    
    """def queryset(self, vRequest):
        qs = super(AdminUsuario, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            return qs.filter(empresa= iEmpresa)
        else:
            return qs.all()"""
    
    
admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Tipo_de_Usuario, AdminTipo_de_Usuario)
admin.site.register(Usuario, AdminUsuario)