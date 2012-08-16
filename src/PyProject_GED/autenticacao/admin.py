'''
Created on Jan 17, 2012

@author: spengler
'''

from django.contrib                 import admin, sites
from django.contrib.auth.admin      import UserAdmin 
from django.contrib.auth.models     import User, Group
from django.contrib.sites.models    import Site

from models                         import Empresa
from models                         import Usuario
from multiAdmin                     import MultiDBModelAdmin #@UnresolvedImport

from PyProject_GED.indice.models    import Indice, Tipo_de_Indice
from PyProject_GED import multiuploader
from PyProject_GED.autenticacao.models import Tipo_de_Usuario


class AdminEmpresa(MultiDBModelAdmin): 
    list_display    = ('id_empresa', 'nome', 'cnpj', 'cep', 'rua', 'numero', 'complemento', 'bairro', 
                       'cidade', 'uf', 'eh_ativo')
    search_fields   = ('id_empresa', 'nome', 'cnpj', 'eh_ativo')
    exclude         = ('id_empresa', 'pasta_raiz') 
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(id_empresa= iEmpresa)
                self.fields['empresa']= iEmpresa
            except:
                return qs.all()
        else:
            return qs.all()
    
class AdminUsuario(MultiDBModelAdmin): 
    list_display    = UserAdmin.list_display + ('empresa', 'is_active')
    search_fields   = UserAdmin.search_fields
    exclude         = ('last_login', 'date_joined', 'is_superuser', 'user_permissions', 
                       'tipo_usuario', 'username') 
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminUsuario,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        form.base_fields['email'].required= True
        return form 
    
    def save_model(self, request, obj, form, change):
        obj.tipo_usuario = Tipo_de_Usuario.objects.all()[0]
        obj.save()

   
class AdminIndice(MultiDBModelAdmin): 
    list_display    = ('id_indice', 'descricao')
    search_fields   = ('id_indice',)
    exclude         = ('id_indice', 'tipo_indice')
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminIndice,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
            #form.base_fields['tipo_indice'].queryset = Tipo_de_Indice.objects.filter(empresa=iEmpresa)
        return form
    
    def save_model(self, request, obj, form, change):
        obj.tipo_indice = Tipo_de_Indice.objects.all()[0]
        obj.save()

admin.site.unregister(User)
admin.site.unregister(Site)
admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Usuario, AdminUsuario)
admin.site.register(Indice, AdminIndice)