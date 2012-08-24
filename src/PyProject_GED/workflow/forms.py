# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django                         import forms
from autenticacao.models            import Usuario #@UnresolvedImport
from autenticacao.models            import Empresa #@UnresolvedImport
from PyProject_GED                  import constantes
from PyProject_GED.seguranca.models import Funcao_Grupo

class FormEncaminharPendencia(forms.Form):
           
    usr_destinatario = forms.ChoiceField(choices=[])
    descricao = forms.Field(widget=forms.Textarea)
    
    def clean_usr_destinatario(self):
        if self.cleaned_data['usr_destinatario'] == 0:
            raise forms.ValidationError('O campo Usuário Destinatário é obrigatório')
        return self.cleaned_data['usr_destinatario']
    
    def clean_descricao(self):
        if self.cleaned_data['descricao'] == '':
            raise forms.ValidationError('O campo Descrição é obrigatório')
        return self.cleaned_data['descricao']
   
    def __init__(self, *args, **kwargs):
        iIDEmpresa= kwargs.pop('iIDEmpresa')
        iEmpresa= Empresa.objects.filter(id_empresa= iIDEmpresa)[0]
        super(FormEncaminharPendencia, self).__init__(*args, **kwargs)  
        self.fields['descricao'].error_messages['required'] = u'O campo Descrição é obrigatório' 
        self.fields['usr_destinatario'].error_messages['required'] = u'O campo Usuário Destinatário é obrigatório'  
        iListaResponsavel= Usuario.objects.filter(empresa= iEmpresa.id_empresa)
        iListaResp = []
        iListaResp.append((0, '- Selecione -'))
        for i in range(len(iListaResponsavel)): 
            iResp = iListaResponsavel[i]
            iNome= iResp.first_name + ' ' + iResp.last_name
            if Funcao_Grupo().possuiAcessoFuncao(iListaResponsavel[i], constantes.cntFuncaoAprovarReprovar):
                iListaResp.append((iResp.id, iNome))    
        self.fields['usr_destinatario'].choices = iListaResp
