'''
Created on Jan 17, 2012

@author: spengler
'''
from django                         import forms
from django.contrib                 import admin
from django.contrib.auth.admin      import UserAdmin 
from django.contrib.auth.models     import User
from django.contrib.sites.models    import Site

from models                         import Empresa
from models                         import Usuario
from multiAdmin                     import MultiDBModelAdmin #@UnresolvedImport

from PyProject_GED.indice.models    import Indice, Tipo_de_Indice
from PyProject_GED.autenticacao.models import Tipo_de_Usuario
from PyProject_GED.historico.models import Log_Usuario
from PyProject_GED.seguranca.models import Grupo, Grupo_Pasta, Grupo_Usuario,\
    Funcao_Grupo, Pasta


class AdminEmpresa(MultiDBModelAdmin): 
    list_display    = ('id_empresa', 'nome', 'cnpj', 'cep', 'rua', 'numero', 'complemento', 'bairro', 
                       'cidade', 'uf', 'eh_ativo', 'eh_publico')
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
        return form
    
    def save_model(self, request, obj, form, change):
        obj.tipo_indice = Tipo_de_Indice.objects.all()[0]
        obj.save()
        
class AdminPasta(MultiDBModelAdmin): 
    list_display    = ('pasta_pai', 'nome', 'diretorio')
    search_fields   = ('pasta_pai', 'nome', 'diretorio',)
    ordering        = ('pasta_pai',)
    exclude         = ('id_pasta',)
        
class AdminLogUsuario(MultiDBModelAdmin): 
    list_display    = ('usuario', 'versao', 'tipo_evento', 'data')
    search_fields   = ('usuario',)
    ordering        = ('data',)
    readonly_fields = ('id_log_usuario', 'usuario', 'versao', 'tipo_evento', 'empresa', 'data')
    exclude         = ('id_log_usuario',)
    
class AdminGrupo(MultiDBModelAdmin): 
    list_display    = ('nome', 'descricao')
    search_fields   = ('nome', 'descricao',)
    ordering        = ('nome',)
    exclude         = ('id_grupo',)
        
class AdminGrupoPasta(MultiDBModelAdmin): 
    list_display    = ('grupo', 'pasta')
    search_fields   = ('grupo', 'pasta')
    ordering        = ('grupo',)  
    exclude         = ('id_grupo_pasta',)  
    
class AdminGrupoUsuario(MultiDBModelAdmin): 
    list_display    = ('grupo', 'usuario')
    search_fields   = ('grupo', 'usuario')
    ordering        = ('grupo',)   
    exclude         = ('id_grupo_usuario',)  
    
class AdminFuncaoGrupo(admin.ModelAdmin): 
    list_display    = ('funcao', 'grupo')
    search_fields   = ('funcao', 'grupo')
    ordering        = ('funcao',)  
    exclude         = ('id_funcao_grupo',)
    
admin.site.unregister(User)
admin.site.unregister(Site)
admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Usuario, AdminUsuario)
admin.site.register(Indice, AdminIndice)
admin.site.register(Log_Usuario, AdminLogUsuario)
admin.site.register(Funcao_Grupo, AdminFuncaoGrupo)
admin.site.register(Grupo, AdminGrupo)
admin.site.register(Grupo_Pasta, AdminGrupoPasta)
admin.site.register(Grupo_Usuario, AdminGrupoUsuario)
admin.site.register(Pasta, AdminPasta)
