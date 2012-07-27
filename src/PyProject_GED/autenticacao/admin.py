'''
Created on Jan 17, 2012

@author: spengler
'''

from django.contrib                 import admin
from django.contrib.auth.admin      import UserAdmin 
from django.contrib.auth.models     import User, Group

from models                         import Empresa
from models                         import Tipo_de_Usuario
from models                         import Usuario
from multiAdmin                     import MultiDBModelAdmin #@UnresolvedImport

from PyProject_GED.indice.models    import Indice, Tipo_de_Indice


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
    
class AdminTipo_de_Usuario(MultiDBModelAdmin): 
    list_display    = ('id_tipo_usuario', 'descricao')
    search_fields   = ('id_tipo_usuario',)
    exclude         = ('id_tipo_usuario',) 

    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminTipo_de_Usuario,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        return form

#    def save_model(self, request, obj, form, change):
#        iEmpresa= Usuario().obtemEmpresaDoUsuario(request.user.id)
#        obj.empresa = iEmpresa
#        obj.save()

class AdminUsuario(MultiDBModelAdmin): 
    list_display    = UserAdmin.list_display + ('empresa', 'tipo_usuario', 'eh_ativo')
    search_fields   = UserAdmin.search_fields
    exclude         = ('last_login', 'date_joined') 
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminUsuario,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
            form.base_fields['tipo_usuario'].queryset = Tipo_de_Usuario.objects.filter(empresa=iEmpresa)
        else:
            iListaAdministradores= Tipo_de_Usuario().obtemListaDeAdministradores() 
            form.base_fields['tipo_usuario'].queryset = Tipo_de_Usuario.objects.filter(id_tipo_usuario__in= iListaAdministradores)
        return form 

   
class AdminIndice(MultiDBModelAdmin): 
    list_display    = ('id_indice', 'descricao')
    search_fields   = ('id_indice',)
    exclude         = ('id_indice',)
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminIndice,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
            form.base_fields['tipo_indice'].queryset = Tipo_de_Indice.objects.filter(empresa=iEmpresa)
        return form

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Tipo_de_Usuario, AdminTipo_de_Usuario)
admin.site.register(Usuario, AdminUsuario)
admin.site.register(Indice, AdminIndice)