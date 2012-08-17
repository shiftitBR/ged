'''
Created on Mar 16, 2012

@author: spengler
'''

from django.contrib.auth.forms import AuthenticationForm

AuthenticationForm.base_fields['username'].max_length = 150 # I guess not needed
AuthenticationForm.base_fields['username'].widget.attrs['maxlength'] = 150 # html
AuthenticationForm.base_fields['username'].validators[0].limit_value = 150