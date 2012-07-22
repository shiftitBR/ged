# -*- coding: utf-8 -*-
'''
Created on Jul 19, 2012

@author: Shift IT | wwww.shiftit.com.br
'''

from django                     import forms
from models                     import Tipo_de_Documento


class FormUploadDeArquivo(forms.Form):
    iListaTipoDocumento= Tipo_de_Documento.objects.filter()
    iListaTipoDoc= []
    iListaTipoDoc.append(('selected', '-----'))
    for i in range(len(iListaTipoDocumento)): 
        iTipoDoc = iListaTipoDocumento[i]
        iListaTipoDoc.append((iTipoDoc.id_tipo_documento, iTipoDoc.descricao)) 
    
    tipo_documento              = forms.ChoiceField(choices=iListaTipoDoc)
    locals()['usr_responsavel'] = forms.CharField(max_length=100)
    locals()['assunto']         = forms.CharField(max_length=100)
    locals()['data_validade']   = forms.DateField()
    locals()['data_descarte']   = forms.DateField()
    locals()['eh_publico']      = forms.BooleanField()
   
    def __init__(self, *args, **kwargs):
        super(FormUploadDeArquivo, self).__init__(*args, **kwargs)  
        self.fields['tipo_documento'].error_messages['required'] = u'O campo Tipo de Documento é obrigatório'   
        self.fields['usr_responsavel'].required = False
        self.fields['assunto'].error_messages['required'] = u'O campo Assunto é obrigatório'
        self.fields['data_validade'].required = False
        self.fields['data_descarte'].required = False
        self.fields['eh_publico'].required = False
        