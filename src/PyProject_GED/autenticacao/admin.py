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


class AdminEmpresa(MultiDBModelAdmin): 
    list_display    = ('id_empresa', 'nome', 'cnpj', 'cep', 'rua', 'numero', 'complemento', 'bairro', 
                       'cidade', 'uf', 'eh_ativo')
    search_fields   = ('id_empresa', 'nome', 'cnpj', 'eh_ativo')
    
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
#    exclude         = ('empresa',) 

#    def save_model(self, request, obj, form, change):
#        iEmpresa= Usuario().obtemEmpresaDoUsuario(request.user.id)
#        obj.empresa = iEmpresa
#        obj.save()

class AdminUsuario(MultiDBModelAdmin): 
    list_display    = UserAdmin.list_display + ('empresa', 'tipo_usuario', 'eh_ativo')
    search_fields   = UserAdmin.search_fields
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminUsuario,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        form.base_fields['tipo_usuario'].queryset = Tipo_de_Usuario.objects.filter(empresa=iEmpresa)
        return form 

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Tipo_de_Usuario, AdminTipo_de_Usuario)
admin.site.register(Usuario, AdminUsuario)