# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django                     import forms
from PyProject_GED.autenticacao.models import Empresa, Usuario


class FormEmail(forms.Form):
    
    destinatarios   = forms.MultipleChoiceField(choices=[])
    assunto         = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Assunto *'}))
    texto           = forms.Field(widget=forms.Textarea)
    
    def clean_descricao(self):
        if self.cleaned_data['texto'] == '':
            raise forms.ValidationError('O campo Descrição é obrigatório')
        return self.cleaned_data['texto']
    
    def clean_destinatarios(self):
        if self.cleaned_data['destinatarios'] == 0:
            raise forms.ValidationError('O campo Destinatários é obrigatório')
        return self.cleaned_data['destinatarios']
    
    def clean_assunto(self):
        if self.cleaned_data['assunto'] == '':
            raise forms.ValidationError('O campo assunto é obrigatório')
        return self.cleaned_data['assunto']
   
    def __init__(self, *args, **kwargs):
        iIDEmpresa= kwargs.pop('iIDEmpresa')
        iEmpresa= Empresa.objects.filter(id_empresa= iIDEmpresa)[0]
        
        iListaDestinatarios= []
        iLista= Usuario().obtemUsuariosComEmailDaEmpresa(iEmpresa)
        for i in range(len(iLista)):
            iListaDestinatarios.append((iLista[i].id, '%s %s' % (iLista[i].first_name, iLista[i].last_name)))
        
        super(FormEmail, self).__init__(*args, **kwargs)  
        self.fields['texto'].error_messages['required'] = u'O campo Descrição é obrigatório' 
        self.fields['assunto'].error_messages['required'] = u'O campo Assunto é obrigatório'  
        self.fields['destinatarios'].error_messages['required'] = u'O campo Destinatários é obrigatório'  
        self.fields['destinatarios'].choices = iListaDestinatarios