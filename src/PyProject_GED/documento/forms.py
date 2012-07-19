'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

import constantes #@UnresolvedImport

from django                     import forms
from django.utils.translation   import ugettext as trans
from django.forms.widgets       import CheckboxInput
from django.contrib.auth.models import User


class FormUploadDeArquivo(forms.Form):
    locals()['tipo_documento']  = forms.CharField(max_length=100)
    locals()['usr_responsavel'] = forms.CharField(max_length=100)
    locals()['assunto']         = forms.CharField(max_length=100)
    locals()['data_validade']   = forms.DateField()
    locals()['data_descarte']   = forms.DateField()
    locals()['eh_publico']      = forms.BooleanField()
    locals()['arquivo']         = forms.FileField()
   
    def __init__(self, *args, **kwargs):
        super(FormUploadDeArquivo, self).__init__(*args, **kwargs)  
        self.fields['tipo_documento'].required = True   
        self.fields['usr_responsavel'].required = False
        self.fields['assunto'].required = True
        self.fields['data_validade'].required = False
        self.fields['data_descarte'].required = False
        self.fields['eh_publico'].required = False
        self.fields['arquivo'].required = True