# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django                     import forms
from models                     import Tipo_de_Documento
from autenticacao.models        import Usuario #@UnresolvedImport
from autenticacao.models        import Empresa #@UnresolvedImport
from PyProject_GED.qualidade.models import Norma

class FormUploadDeArquivo(forms.Form):
        
    tipo_documento  = forms.ChoiceField(choices=[])
    usr_responsavel = forms.ChoiceField(choices=[])
    norma           = forms.MultipleChoiceField(choices=[])
    assunto         = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Assunto *'}))
    data_validade   = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Data de Validade'}))
    data_descarte   = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Data de Descarte'}))
    eh_publico      = forms.BooleanField()
    
    def clean_tipo_documento(self):
        if self.cleaned_data['tipo_documento'] == 0:
            raise forms.ValidationError('O campo Tipo de Documento é obrigatório')
        return self.cleaned_data['tipo_documento']
    
    def clean_usr_responsavel(self):
        if self.cleaned_data['usr_responsavel'] == 0:
            raise forms.ValidationError('O campo Usuário Responsável é obrigatório')
        return self.cleaned_data['usr_responsavel']
    
    def clean_assunto(self):
        if self.cleaned_data['assunto'] == '':
            raise forms.ValidationError('O campo assunto é obrigatório')
        return self.cleaned_data['assunto']
   
    def __init__(self, *args, **kwargs):
        iIDEmpresa= kwargs.pop('iIDEmpresa')
        iEmpresa= Empresa.objects.filter(id_empresa= iIDEmpresa)[0]
        
        iListaDeUsuariosResponsaveis= []
        iListaDeUsuariosResponsaveis.append(('Selecione', 'Usuário Responsável *'))
        iLista= Usuario().obtemUsuariosDaEmpresa(iEmpresa)
        for i in range(len(iLista)):
            iListaDeUsuariosResponsaveis.append((iLista[i].id, '%s %s' % (iLista[i].first_name, iLista[i].last_name)))
        
        iListaDeTiposDeDocumento= []
        iListaDeTiposDeDocumento.append(('Selecione', 'Tipo de Documento *'))
        iLista= Tipo_de_Documento().obtemListaTipoDocumentoDaEmpresa(iEmpresa.id_empresa)
        for i in range(len(iLista)):
            iListaDeTiposDeDocumento.append((iLista[i].id_tipo_documento, '%s' % iLista[i].descricao))
            
        iListaNormas= []
        iLista = Norma.objects.filter(empresa= iEmpresa.id_empresa).order_by('numero')
        for i in range(len(iLista)):
            iListaNormas.append((iLista[i].id_norma, '%s %s' % (iLista[i].numero, iLista[i].descricao)))
        
        super(FormUploadDeArquivo, self).__init__(*args, **kwargs)          
        self.fields['tipo_documento'].error_messages['required'] = u'O campo Tipo de Documento é obrigatório' 
        self.fields['assunto'].error_messages['required'] = u'O campo Assunto é obrigatório'  
        self.fields['usr_responsavel'].error_messages['required'] = u'O campo Usuário Responsável é obrigatório'  
        self.fields['data_validade'].required = False
        self.fields['data_descarte'].required = False
        self.fields['eh_publico'].required = False
        self.fields['norma'].choices = iListaNormas
        self.fields['tipo_documento'].choices = iListaDeTiposDeDocumento
        self.fields['usr_responsavel'].choices = iListaDeUsuariosResponsaveis
        
class FormCheckin(forms.Form):

    descricao = forms.Field(widget=forms.Textarea)
    
    def clean_descricao(self):
        if self.cleaned_data['descricao'] == '':
            raise forms.ValidationError('O campo Descrição é obrigatório')
        return self.cleaned_data['descricao']
   
    def __init__(self, *args, **kwargs):
        super(FormCheckin, self).__init__(*args, **kwargs)  
        self.fields['descricao'].error_messages['required'] = u'O campo Descrição é obrigatório' 
        