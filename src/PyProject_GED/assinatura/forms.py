# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django                     import forms
from controle                   import Controle as  AssinaturaControle 

class FormUploadCertificado(forms.Form):
    senha       = forms.CharField(max_length=30, widget=forms.PasswordInput)
    certificado = forms.FileField(label='Selecione o Certificado Digital', help_text='Certificado')
   
    def __init__(self, *args, **kwargs):        
        super(FormUploadCertificado, self).__init__(*args, **kwargs)
        self.fields['senha'].error_messages['required'] = u'O campo Senha é obrigatório'
        self.fields['certificado'].error_messages['required'] = u'O campo Certificado é obrigatório'  
        
    def clean_senha(self):
        if self.cleaned_data['senha'] == '':
            raise forms.ValidationError('O campo senha é obrigatório')
        return self.cleaned_data['senha']

    def clean_certificado(self):
        iCertificado = self.cleaned_data['certificado']
        if iCertificado == '':
            raise forms.ValidationError('O campo certificado é obrigatório')
        elif not AssinaturaControle().verificaExtCertificadoValido(iCertificado):
            raise forms.ValidationError('Adicione um Certificado válido')
        return self.cleaned_data['certificado']