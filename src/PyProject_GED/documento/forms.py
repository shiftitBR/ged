# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django                     import forms
from models                     import Tipo_de_Documento
from autenticacao.models        import Usuario #@UnresolvedImport
from autenticacao.models        import Empresa #@UnresolvedImport
from PyProject_GED.indice.models import Indice

class FormUploadDeArquivo(forms.Form):
            
    iListaResponsavel= Usuario.objects.all()
    iListaResp = []
    iListaResp.append((0, '- Selecione -'))
    for i in range(len(iListaResponsavel)): 
        iResp = iListaResponsavel[i]
        iNome= iResp.first_name + ' ' + iResp.last_name
        iListaResp.append((iResp.id, iNome)) 
                   
    tipo_documento  = forms.ModelChoiceField(queryset=Tipo_de_Documento.objects.all())
    usr_responsavel = forms.ModelChoiceField(iListaResp)
    assunto         = forms.CharField(max_length=100)
    data_validade   = forms.DateField()
    data_descarte   = forms.DateField()
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
        super(FormUploadDeArquivo, self).__init__(*args, **kwargs)          
        self.fields['tipo_documento'].error_messages['required'] = u'O campo Tipo de Documento é obrigatório' 
        self.fields['assunto'].error_messages['required'] = u'O campo Assunto é obrigatório'  
        self.fields['usr_responsavel'].error_messages['required'] = u'O campo Usuário Responsável é obrigatório'  
        self.fields['data_validade'].required = False
        self.fields['data_descarte'].required = False
        self.fields['eh_publico'].required = False
        self.fields['usr_responsavel'].queryset = Usuario.objects.filter(empresa= iEmpresa.id_empresa)
        self.fields['tipo_documento'].queryset = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)
        
        
class FormCheckin(forms.Form):

    descricao = forms.Field(widget=forms.Textarea)
    
    def clean_descricao(self):
        if self.cleaned_data['descricao'] == '':
            raise forms.ValidationError('O campo Descrição é obrigatório')
        return self.cleaned_data['descricao']
   
    def __init__(self, *args, **kwargs):
        super(FormCheckin, self).__init__(*args, **kwargs)  
        self.fields['descricao'].error_messages['required'] = u'O campo Descrição é obrigatório' 
        