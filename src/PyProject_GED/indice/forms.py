# -*- coding: utf-8 -*-
'''
Created on Aug 2, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django                             import forms
from PyProject_GED.autenticacao.models  import Usuario, Empresa
from PyProject_GED.documento.models import Estado_da_Versao, Tipo_de_Documento

class FormBuscaDocumento(forms.Form):
              
    protocolo           = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Protocolo'}))
    conteudo            = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Conteúdo'}))
    assunto             = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Assunto'}))
    data_criacao_inicial= forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Data de Criação [Apartir]'}))
    data_criacao_final  = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Data de Criação [Até]'}))
    usuario_responsavel = forms.ChoiceField(choices=[])
    usuario_criador     = forms.ChoiceField(choices=[])
    normas              = forms.ChoiceField(choices=[])
    tipo_documento      = forms.ChoiceField(choices=[])
    estado              = forms.ChoiceField(choices=[])
          
    def __init__(self, *args, **kwargs):
        iIDEmpresa= kwargs.pop('iIDEmpresa')
        iEmpresa= Empresa.objects.filter(id_empresa= iIDEmpresa)[0]
        
        iListaDeUsuariosResponsaveis= []
        iListaDeUsuariosResponsaveis.append(('selected', 'Usuário Responsável'))
        iLista= Usuario().obtemUsuariosDaEmpresa(iEmpresa)
        for i in range(len(iLista)):
            iListaDeUsuariosResponsaveis.append((iLista[i].id, '%s %s' % (iLista[i].first_name, iLista[i].last_name)))
        
        iListaDeUsuariosCriadores= []
        iListaDeUsuariosCriadores.append(('selected', 'Usuário Criador'))
        for i in range(len(iLista)):
            iListaDeUsuariosCriadores.append((iLista[i].id, '%s %s' % (iLista[i].first_name, iLista[i].last_name)))
        
        iListaDeNormas= []
        iListaDeNormas.append(('selected', 'Norma da Qualidade'))
        
        iListaDeTiposDeDocumento= []
        iListaDeTiposDeDocumento.append(('selected', 'Tipo de Documento'))
        iLista= Tipo_de_Documento().obtemListaTipoDocumentoDaEmpresa(iEmpresa.id_empresa)
        for i in range(len(iLista)):
            iListaDeTiposDeDocumento.append((iLista[i].id_tipo_documento, '%s' % iLista[i].descricao))
        
        iListaDeEstados= []
        iListaDeEstados.append(('selected', 'Estado do Documento'))
        iLista= Estado_da_Versao().obtemEstadosDaVersao()
        for i in range(len(iLista)):
            iListaDeEstados.append((iLista[i].id_estado_da_versao, '%s' % iLista[i].descricao))
        
        super(FormBuscaDocumento, self).__init__(*args, **kwargs)  
        self.fields['usuario_responsavel'].choices = iListaDeUsuariosResponsaveis
        self.fields['usuario_criador'].choices = iListaDeUsuariosCriadores
        self.fields['normas'].choices = iListaDeNormas
        self.fields['tipo_documento'].choices = iListaDeTiposDeDocumento
        self.fields['estado'].choices = iListaDeEstados
        
        