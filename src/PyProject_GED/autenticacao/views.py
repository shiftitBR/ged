from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth                import authenticate 
from django.contrib.auth                import logout as auth_logout
from django.contrib.auth                import login as auth_login
from django.http                        import HttpResponseRedirect
from PyProject_GED.seguranca.models     import Firewall

import constantes #@UnresolvedImport
from PyProject_GED.autenticacao.models import Usuario

def login(vRequest, vTitulo):
    
    if vRequest.POST:
        username= vRequest.POST.get('username')
        password= vRequest.POST.get('password')
        
        try:
            client_address = vRequest.META['HTTP_X_FORWARDED_FOR']  # case server 200.000.02.001
        except:
            client_address = vRequest.META['REMOTE_ADDR']           # case localhost ou 127.0.0.1
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if Firewall().verificaIP(client_address, Usuario().obtemUsuario(user).empresa):
                    auth_login(vRequest, user)
                    return HttpResponseRedirect('/documentos/')
                else: 
                    auth_logout(vRequest)
                    return HttpResponseRedirect('/login_error/'+ str(constantes.cntTipoErroIpBloqueado))
            else:
                return HttpResponseRedirect('/login_error/' + str(constantes.cntTipoErroInativo))
        else:
            return HttpResponseRedirect('/login_error/'+ str(constantes.cntTipoErroSenhaUser))
    
    return render_to_response(
        'login/login.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def logout(vRequest, vTitulo):
    auth_logout(vRequest)
    return HttpResponseRedirect('/')

    return render_to_response(
        'logout/logout.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
    
def login_error(vRequest, vTitulo, vTipoErro=None):
    
    return render_to_response(
        'login/login_error.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )