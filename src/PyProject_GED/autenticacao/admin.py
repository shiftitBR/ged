'''
Created on Jan 17, 2012

@author: spengler
'''

from django.contrib                 import admin
from django.contrib.admin.sites     import AdminSite
from django.contrib.admin.options   import ModelAdmin
from django.contrib.auth.admin      import UserAdmin 

from models                         import Empresa
from models                         import Tipo_de_Usuario
from models                         import Usuario
from PyProject_GED                  import oControle

from multiAdmin                     import MultiDBModelAdmin #@UnresolvedImport


MultiDBModelAdmin.using= oControle.getBanco()
 
class AdminEmpresa(MultiDBModelAdmin): 
    list_display    = ('id_empresa', 'nome', 'cnpj', 'cep', 'rua', 'numero', 'complemento', 'bairro', 
                       'cidade', 'uf', 'banco', 'eh_ativo')
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
    
    
admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Tipo_de_Usuario, AdminTipo_de_Usuario)
admin.site.register(Usuario, AdminUsuario)