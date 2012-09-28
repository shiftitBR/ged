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
from PyProject_GED.autenticacao.forms   import FormConfiguracoesDeUsuario,\
    FormCadastroDeContato

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
                iUsuario= Usuario().obtemUsuario(user)
                if Usuario().ehContato(iUsuario):
                    messages.warning(vRequest, 'Este Usuário está cadastrado como Contato, não sendo permitido efetuar login no sistema.')
                elif user.is_active:
                    if Firewall().verificaIP(client_address, iUsuario.empresa):
                        if iUsuario.empresa.eh_ativo:
                            auth_login(vRequest, user)
                            vRequest.session.set_expiry(6000)
                            vRequest.session['IDEmpresa']       = iUsuario.empresa.id_empresa
                            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoLogin, iUsuario.id, vRequest.session['IDEmpresa'])
                            return HttpResponseRedirect('/documentos/')
                        else:
                            messages.warning(vRequest, 'Esta Empresa está Inativa. Para mais informações entre em contato com o administrador.')
                    else: 
                        oControle.getLogger().warning('O IP_Address: ' + str(client_address) + ' foi recusado!')
                        auth_logout(vRequest)
                        messages.warning(vRequest, 'Este endereço de IP está bloqueado. Para mais informações entre em contato com o administrador.')
                else:
                    messages.warning(vRequest, 'Este Usuário está Inativo. Para mais informações entre em contato com o administrador.')
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
    
def trocar_senha(vRequest, vTitulo):
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
    else:
        iUsuario= None
        
    if vRequest.POST:
        try:
            form = FormConfiguracoesDeUsuario(vRequest.POST, instance= iUsuario)
            if form.is_valid():
                iUsuario = form.save(commit=True)
                
                return HttpResponseRedirect('/')
            else:
                form = FormConfiguracoesDeUsuario(vRequest.POST)
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post trocar_senha: ' + str(e))
            return False
    else:
        form = FormConfiguracoesDeUsuario(instance= iUsuario)
        
    return render_to_response(
        'senha/trocar_senha.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def contato(vRequest, vTitulo, vRedireciona=None):
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
    else:
        iUsuario= None
    
    if vRequest.POST:
        try:
            form = FormCadastroDeContato(vRequest.POST)
            if form.is_valid():
                Usuario().adicionaContato(iUsuario.empresa, 
                                          vRequest.POST.get('first_name'), 
                                          vRequest.POST.get('last_name'), 
                                          vRequest.POST.get('email'))
                Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoCadastraContato, iUsuario.id, 
                                          vRequest.session['IDEmpresa'])
                if int(vRedireciona) == constantes.cntRedirecionaEmail:
                    return HttpResponseRedirect('/email/')
                elif int(vRedireciona) == constantes.cntRedirecionaPublicacao: 
                    return HttpResponseRedirect('/publicar/')
            else:
                form = FormCadastroDeContato(vRequest.POST)
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post contato: ' + str(e))
            return False
    else:
        form = FormCadastroDeContato()
    return render_to_response(
        'contato/contato.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )