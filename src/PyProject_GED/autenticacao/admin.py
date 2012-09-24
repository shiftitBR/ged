# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

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
    Funcao_Grupo, Pasta, Firewall, Firewall_Grupo, Funcao
from PyProject_GED.qualidade.models import Tipo_de_Norma, Norma
from PyProject_GED.documento.models import Tipo_de_Documento
from PyProject_GED.workflow.models  import Workflow, Etapa_do_Workflow
from PyProject_GED import constantes

import logging
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

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
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminEmpresa: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
class AdminUsuario(MultiDBModelAdmin): 
    list_display    = UserAdmin.list_display + ('empresa', 'is_active')
    search_fields   = UserAdmin.search_fields
    exclude         = ('last_login', 'date_joined', 'is_superuser', 'user_permissions', 
                       'tipo_usuario', 'username') 
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(empresa= iEmpresa.id_empresa)
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminUsuario: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminUsuario,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        form.base_fields['email'].required= True
        return form 
    
    def save_model(self, request, obj, form, change):
        obj.tipo_usuario = Tipo_de_Usuario.objects.filter(id_tipo_de_usuario= constantes.cntTipoUsuarioSistema)[0]
        obj.save()
        

"""class AdminContato(MultiDBModelAdmin): 
    list_display    = UserAdmin.list_display + ('empresa', 'is_active')
    search_fields   = UserAdmin.search_fields
    exclude         = ('last_login', 'date_joined', 'is_superuser', 'user_permissions', 
                       'tipo_usuario', 'username') 
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(id_empresa= iEmpresa, tipo_usuario__id_tipo_usuario= constantes.cntTipoUsuarioContato)
                self.fields['empresa']= iEmpresa
            except:
                return qs.all()
        else:
            return qs.all()
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminUsuario,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        form.base_fields['email'].required= True
        return form 
    
    def save_model(self, request, obj, form, change):
        obj.tipo_usuario = Tipo_de_Usuario.objects.filter(constantes.cntTipoUsuarioContato)[0]
        obj.save()"""

   
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
    list_display    = ('nome', 'pasta_pai')
    search_fields   = ('pasta_pai', 'nome', )
    ordering        = ('pasta_pai',)
    exclude         = ('id_pasta', 'diretorio', )
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(usuario__empresa= iEmpresa.id_empresa)
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminPasta: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminPasta,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['pasta_pai'].queryset = Pasta.objects.filter(empresa=iEmpresa.id_empresa)
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        return form
    
class AdminLogUsuario(MultiDBModelAdmin): 
    list_display    = ('usuario', 'versao', 'tipo_evento', 'data')
    search_fields   = ('usuario',)
    ordering        = ('data',)
    readonly_fields = ('id_log_usuario', 'usuario', 'versao', 'tipo_evento', 'data', 'empresa')
    exclude         = ('id_log_usuario',)
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(usuario__empresa= iEmpresa.id_empresa)
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminLogUsuario: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
class AdminGrupo(MultiDBModelAdmin): 
    list_display    = ('nome', 'descricao')
    search_fields   = ('nome', 'descricao',)
    ordering        = ('nome',)
    exclude         = ('id_grupo',)
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminGrupo,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        return form
        
class AdminGrupoPasta(MultiDBModelAdmin): 
    list_display    = ('grupo', 'pasta')
    search_fields   = ('grupo', 'pasta')
    ordering        = ('grupo',)  
    exclude         = ('id_grupo_pasta',)  
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(grupo__empresa= iEmpresa.id_empresa)
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminGrupoPasta: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminGrupoPasta,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['grupo'].queryset  = Grupo.objects.filter(empresa= iEmpresa.id_empresa)
            form.base_fields['pasta'].queryset  = Pasta.objects.filter(empresa= iEmpresa.id_empresa)
        return form
    
class AdminGrupoUsuario(MultiDBModelAdmin): 
    list_display    = ('grupo', 'usuario')
    search_fields   = ('grupo', 'usuario')
    ordering        = ('grupo',)   
    exclude         = ('id_grupo_usuario',)  
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(grupo__empresa= iEmpresa.id_empresa)
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminGrupoUsuario: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminGrupoUsuario,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['grupo'].queryset      = Grupo.objects.filter(empresa= iEmpresa.id_empresa)
            form.base_fields['usuario'].queryset    = Usuario.objects.filter(empresa= iEmpresa.id_empresa)
        return form

class AdminFuncaoGrupoForm(forms.ModelForm):
    funcoes = forms.ModelMultipleChoiceField(
        queryset=Funcao.objects.all(), 
        required=True,
        widget=FilteredSelectMultiple(
            verbose_name=('Funcoes'),
            is_stacked=False
        )
    )

    class Meta:
        model = Grupo
        list_display    = ('grupo',)
        search_fields   = ('grupo',)
        ordering        = ('grupo',)  
        exclude         = ('funcao', 'id_funcao_grupo',)

    def __init__(self, *args, **kwargs):
        super(AdminFuncaoGrupoForm, self).__init__(*args, **kwargs)

        if self.instance.id_funcao_grupo != None:
            iListaFuncaoGrupo= Funcao_Grupo.objects.filter(grupo= self.instance.grupo)
            iListaFuncaoIDs= []
            for iFuncaoGrupo in iListaFuncaoGrupo:
                iListaFuncaoIDs.append(iFuncaoGrupo.funcao.id_funcao)
            self.fields['funcoes'].initial = Funcao.objects.filter(id_funcao__in= iListaFuncaoIDs)
            iListaGrupos= []
            iLista = Grupo.objects.filter(id_grupo= self.instance.grupo.id_grupo)
            for iGrupo in iLista:
                iListaGrupos.append((iGrupo.id_grupo, '%s' % iGrupo.nome))
            
            self.fields['grupo'].choices = iListaGrupos

class AdminFuncaoGrupo(MultiDBModelAdmin): 
    list_display    = ('grupo',)
    search_fields   = ('grupo',)
    ordering        = ('grupo',)  
    
    form = AdminFuncaoGrupoForm
         
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            iListaFuncaoGrupo= Funcao_Grupo.objects.filter(grupo__empresa= iEmpresa.id_empresa).order_by('grupo')
        else:
            iListaFuncaoGrupo= Funcao_Grupo.objects.order_by('grupo')
        iListaGrupos= []
        iListaFuncaoGrupoIDs= []
        for iFuncaoGrupo in iListaFuncaoGrupo:
            if iFuncaoGrupo.grupo not in iListaGrupos:
                iListaGrupos.append(iFuncaoGrupo.grupo)
                iListaFuncaoGrupoIDs.append(iFuncaoGrupo.id_funcao_grupo)
        return qs.filter(id_funcao_grupo__in = iListaFuncaoGrupoIDs)
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminFuncaoGrupo,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
            iLista = Funcao_Grupo().obtemListaDeGruposSemFuncao(iEmpresa)
        else:
            iLista = Funcao_Grupo().obtemListaDeGruposSemFuncao()
        iListaGrupos= []
        for iGrupo in iLista:
            iListaGrupos.append((iGrupo.id_grupo, '%s' % iGrupo.nome))
        form.base_fields['grupo'].choices = iListaGrupos
        return form
    
    def save_model(self, vRequest, obj, form, change):
        iListaFuncoes= vRequest.POST.getlist('funcoes')
        iGrupo= vRequest.POST.get('grupo')
        Funcao_Grupo().excluiFuncoesDoGrupo(None, iGrupo)
        for iFuncao in iListaFuncoes:
            Funcao_Grupo().criaFuncao_Grupo(None, None, iFuncao, iGrupo)

class AdminTipoNorma(MultiDBModelAdmin): 
    list_display    = ('descricao', 'empresa')
    search_fields   = ('descricao', 'empresa')
    ordering        = ('descricao',)  
    exclude         = ('id_tipo_norma',)
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminTipoNorma,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        return form
    
class AdminNorma(MultiDBModelAdmin): 
    list_display    = ('numero', 'descricao', 'tipo_norma', 'norma_pai', 'empresa')
    search_fields   = ('norma_pai', 'descricao', 'numero', 'tipo_norma', 'empresa')
    ordering        = ('numero',)  
    exclude         = ('id_norma',)
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminNorma,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
            form.base_fields['tipo_norma'].queryset = Tipo_de_Norma.objects.filter(empresa=iEmpresa.id_empresa)
            form.base_fields['norma_pai'].queryset = Norma.objects.filter(empresa=iEmpresa.id_empresa)
        return form
    
class AdminFirewall(MultiDBModelAdmin): 
    list_display    = ('ip', 'descricao')
    search_fields   = ('ip', 'descricao', 'empresa')
    ordering        = ('ip',)  
    exclude         = ('id_firewall',)
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminFirewall,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        return form
    
class AdminFirewallGrupo(MultiDBModelAdmin): 
    list_display    = ('firewall', 'grupo')
    search_fields   = ('firewall', 'grupo')
    ordering        = ('firewall',)  
    exclude         = ('id_firewall_grupo',)
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(grupo__empresa= iEmpresa.id_empresa)
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminFirewallGrupo: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminFirewallGrupo,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['firewall'].queryset   = Firewall.objects.filter(empresa= iEmpresa.id_empresa)
            form.base_fields['grupo'].queryset      = Grupo.objects.filter(empresa= iEmpresa.id_empresa)
        return form
    
class AdminWorkflow(MultiDBModelAdmin): 
    list_display    = ('descricao', 'tipo_de_documento', 'pasta', 'empresa')
    search_fields   = ('descricao', 'tipo_de_documento', 'pasta')
    ordering        = ('descricao',)  
    exclude         = ('id_workflow',)
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminWorkflow,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['tipo_de_documento'].queryset   = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)
            form.base_fields['pasta'].queryset  = Pasta.objects.filter(empresa= iEmpresa.id_empresa)
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        return form
    
class AdminEtapaWorkflow(MultiDBModelAdmin): 
    list_display    = ('ordem_da_etapa', 'descricao', 'workflow', 'grupo', 'tipo_de_pendencia', 'eh_multipla')
    search_fields   = ('ordem_da_etapa', 'descricao', 'workflow', 'grupo', 'tipo_de_pendencia', 'eh_multipla')
    ordering        = ('workflow', 'ordem_da_etapa', 'descricao',)  
    exclude         = ('id_etapa_do_workflow', 'ordem_da_etapa')
    
    def queryset(self, vRequest):
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(grupo__empresa= iEmpresa.id_empresa)
            except Exception, e:
                logging.getLogger('PyProject_GED.controle').warning('Nao foi possivel AdminEtapaWorkflow: ' + str(e))
                return qs.all()
        else:
            return qs.all()
    
    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminEtapaWorkflow,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['workflow'].queryset   = Workflow.objects.filter(empresa= iEmpresa.id_empresa)
            form.base_fields['grupo'].queryset  = Grupo.objects.filter(empresa= iEmpresa.id_empresa)
        return form   

class AdminTipoDocumento(MultiDBModelAdmin): 
    list_display    = ('descricao', 'empresa')
    search_fields   = ('descricao', 'empresa')
    ordering        = ('descricao',)  
    exclude         = ('id_tipo_documento', 'eh_nativo')

    def get_form(self, vRequest, obj=None, **kwargs):
        form = super(AdminTipoDocumento,self).get_form(vRequest, obj,**kwargs)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            form.base_fields['empresa'].queryset = Empresa.objects.filter(id_empresa=iEmpresa.id_empresa)
        return form

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
admin.site.register(Tipo_de_Norma, AdminTipoNorma)
admin.site.register(Norma, AdminNorma)
admin.site.register(Firewall, AdminFirewall)
admin.site.register(Firewall_Grupo, AdminFirewallGrupo)
admin.site.register(Workflow, AdminWorkflow)
admin.site.register(Etapa_do_Workflow, AdminEtapaWorkflow)
admin.site.register(Tipo_de_Documento, AdminTipoDocumento)
