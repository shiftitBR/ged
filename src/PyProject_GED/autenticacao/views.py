# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth                import authenticate 
from django.contrib.auth                import logout as auth_logout
from django.contrib.auth                import login as auth_login
from django.http                        import HttpResponseRedirect
from django.contrib                     import messages

from PyProject_GED.seguranca.models     import Firewall
from PyProject_GED                      import oControle, constantes
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.historico.models     import Log_Usuario

def login(vRequest, vTitulo):
    
    if vRequest.POST:
        try:
            
            username= vRequest.POST.get('username')
            password= vRequest.POST.get('password')
            
            try:
                client_address = vRequest.META['HTTP_X_FORWARDED_FOR']
            except:
                client_address = vRequest.META['REMOTE_ADDR']
                
            user = authenticate(username=username, password=password)
            if user is not None:
                if not Usuario().obtemUsuario(user).empresa.eh_ativo:
                    messages.warning(vRequest, 'Esta Empresa está inativa. Para mais informações, entre em contato com o administrador.')
                if user.is_active:
                    iUsuario= Usuario().obtemUsuario(user)
                    if Firewall().verificaIP(client_address, iUsuario.empresa):
                        auth_login(vRequest, user)
                        vRequest.session.set_expiry(6000)
                        vRequest.session['IDEmpresa']       = iUsuario.empresa.id_empresa
                        Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoLogin, iUsuario.id, vRequest.session['IDEmpresa'])
                        return HttpResponseRedirect('/documentos/')
                    else: 
                        oControle.getLogger().warning('O IP_Address: ' + str(client_address) + ' foi recusado!')
                        auth_logout(vRequest)
                        messages.warning(vRequest, 'Este endereço de IP está bloqueado. Para mais informações entre em contato com o administrador.')
                else:
                    messages.warning(vRequest, 'Esta Usuário está Inativo. Para mais informações entre em contato com o administrador.')
            else:
                messages.warning(vRequest, 'E-mail e/ou Senha incorreto(s). Digite novamente seu E-mail e Senha para efetuar o login.')
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel get login: ' + str(e))
            return False
    
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
    