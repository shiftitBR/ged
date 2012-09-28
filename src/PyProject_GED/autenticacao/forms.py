# -*- coding: utf-8 -*-
'''
Created on Jan 30, 2012

@author: spengler
'''

from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.forms  import AuthenticationForm
from django.contrib.auth.models import User
from django                     import forms
from django.utils.translation   import ugettext as trans
from PyProject_GED.autenticacao.models import Usuario

class SignUpForm(AuthenticationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label='Email address', max_length=75)
    
    class Meta:
        model = User
        fields = ('username', 'email',) 

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except User.DoesNotExist:
            return email
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
            
        return user   
    
class FormConfiguracoesDeUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'password')

    confirme_a_senha = forms.CharField(
        max_length=30, widget=forms.PasswordInput
        )
    
    senha_atual = forms.CharField(
        max_length=30, widget=forms.PasswordInput
        )

    def __init__(self, *args, **kwargs):        
        self.base_fields['password'].help_text = trans('Informe uma senha segura')
        self.base_fields['password'].widget = forms.PasswordInput()
        
        super(FormConfiguracoesDeUsuario, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'senha_atual',
            'password',
            'confirme_a_senha']
        self.fields['confirme_a_senha'].label = trans('Confirme a senha')
        self.fields['senha_atual'].label = trans('Senha atual')
        self.fields['password'].widget.attrs.update({'class' : 'password'})
        
    def clean_senha_atual(self):
        usuario = super(FormConfiguracoesDeUsuario, self).save(commit=False)
        if not usuario.check_password(self.cleaned_data['senha_atual']):
            raise forms.ValidationError('Senha atual incorreta!')
        return self.cleaned_data['senha_atual']
        
    def clean_confirme_a_senha(self):
        if self.cleaned_data['confirme_a_senha'] != self.cleaned_data['password']:
            raise forms.ValidationError('Confirmação da senha não confere!')
        return self.cleaned_data['confirme_a_senha']

    def save(self, commit=True):
        usuario = super(FormConfiguracoesDeUsuario, self).save(commit=False)
        usuario.password = self.data['confirme_a_senha']
        if commit:
            usuario.save()

        return usuario      
    
class FormCadastroDeContato(forms.Form):
    class Meta:
        fields = ('first_name', 'last_name', 'email')

    email       = forms.EmailField(label='E-mail', max_length=75)
    first_name  = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Primeiro Nome *'}))
    last_name   = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Último Nome *'}))

    def __init__(self, *args, **kwargs):        
        super(FormCadastroDeContato, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'email']
        self.fields['first_name'].label = trans('Primeiro Nome')
        self.fields['last_name'].label  = trans('Ultimo Nome')
        self.fields['email'].label      = trans('E-mail')
        self.fields['first_name'].error_messages['required']    = u'O campo Primeiro Nome é obrigatório' 
        self.fields['last_name'].error_messages['required']     = u'O campo Último Nome é obrigatório' 
        
    def clean_first_name(self):
        if self.cleaned_data['first_name']=='':
            raise forms.ValidationError('O campo Primeiro Nome é obrigatório!')
        return self.cleaned_data['first_name']
        
    def clean_last_name(self):
        if self.cleaned_data['last_name']=='':
            raise forms.ValidationError('O campo Último Nome é obrigatório!')
        return self.cleaned_data['last_name']
        