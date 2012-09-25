# -*- coding: utf-8 -*- 
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.core.mail                   import EmailMessage
from django.conf                        import settings

from PyProject_GED.documento.models     import Versao
from PyProject_GED.autenticacao.models  import Usuario, Empresa
from PyProject_GED.envioemail.forms     import FormEmail
from PyProject_GED                      import oControle, constantes
from objetos_auxiliares                 import Destinatario
from PyProject_GED.historico.models     import Historico, Log_Usuario
from PyProject_GED.envioemail.models    import Publicacao, Publicacao_Documento, Publicacao_Usuario
from PyProject_GED.documento.controle   import Controle as DocumentoControle

import os
from django.http import HttpResponseRedirect

def email(vRequest, vTitulo):
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
    iEmpresa= Empresa.objects.filter(id_empresa= vRequest.session['IDEmpresa'])[0] 
    iListaVersao= vRequest.session['ListaVersao'].split('-')[:-1]
    iListaDestinatarios= []
    iLista= Usuario().obtemUsuariosComEmailDaEmpresa(iEmpresa)
    for i in range(len(iLista)):
        iDestinatario= Destinatario()
        iDestinatario.id= iLista[i].id
        iDestinatario.nome=  '%s %s' % (iLista[i].first_name, iLista[i].last_name)
        iListaDestinatarios.append(iDestinatario)
    iVersoes= []
    for i in range(len(iListaVersao)):
        iVersao= Versao().obtemVersao(int(iListaVersao[i]))
        iVersoes.append(iVersao)
        
    if vRequest.POST:
        try :
            form = FormEmail(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
            if form.is_valid():
                iAssunto        = vRequest.POST.get('assunto')
                iTexto          = vRequest.POST.get('texto')
                iDestinatarios  = vRequest.POST.getlist('destinatarios')

                try:
                    if settings.EMAIL:
                        email           = EmailMessage()
                        email.subject   = iAssunto
                        email.body      = iTexto
                        email.from_email= iUsuario.email
                        for i in range(len(iDestinatarios)):
                            email.to.append(Usuario().obtemUsuarioPeloID(iDestinatarios[i]).email)
                        for i in range(len(iVersoes)):
                            iArquivo= iVersoes[i].upload
                            if iVersoes[i].eh_assinado:
                                iFileAnexo  = DocumentoControle().comprimiArquivoAssinado(str(iArquivo.image))
                                iFile       = open(str(iFileAnexo),"rb")
                                email.attach(filename = DocumentoControle().obtemNomeZipado(str(iArquivo.image)), content = iFile.read())
                            else:
                                iFileAnexo = iArquivo.image
                                iFile = open(str(iFileAnexo),"rb")
                                email.attach(filename = iArquivo.filename, content = iFile.read())
                            iFile.close()
                        email.send()
                        for i in range(len(iVersoes)):
                            Historico().salvaHistorico(iVersoes[i].id_versao, constantes.cntEventoHistoricoEmail, 
                                           iUsuario.id, vRequest.session['IDEmpresa'])
                            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoEmail, iUsuario.id, 
                                    vRequest.session['IDEmpresa'], vIDVersao=iVersoes[i].id_versao)
                        return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoEmail) + '/')
                except Exception, e:
                    oControle.getLogger().error('Nao foi possivel post email: ' + str(e))
                    return False
                else:
                    form = FormEmail(iIDEmpresa=vRequest.session['IDEmpresa'])
            else:
                form = FormEmail(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post email: ' + str(e))
            return False
    else: 
        form = FormEmail(iIDEmpresa=vRequest.session['IDEmpresa'])
        
    return render_to_response(
        'email/email.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
    
def publicar(vRequest, vTitulo):
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
    iEmpresa= Empresa.objects.filter(id_empresa= vRequest.session['IDEmpresa'])[0] 
    iListaVersao= vRequest.session['ListaVersao'].split('-')[:-1]
    iListaDestinatarios= []
    iLista= Usuario().obtemUsuariosComEmailDaEmpresa(iEmpresa)
    for i in range(len(iLista)):
        iDestinatario= Destinatario()
        iDestinatario.id= iLista[i].id
        iDestinatario.nome=  '%s %s' % (iLista[i].first_name, iLista[i].last_name)
        iListaDestinatarios.append(iDestinatario)
    iVersoes= []
    for i in range(len(iListaVersao)):
        iVersao= Versao().obtemVersao(int(iListaVersao[i]))
        iVersoes.append(iVersao)
        
    if vRequest.POST:
        try :
            form = FormEmail(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
            if form.is_valid():
                iAssunto        = vRequest.POST.get('assunto')
                iTexto          = vRequest.POST.get('texto')
                iDestinatarios  = vRequest.POST.getlist('destinatarios')
                
                try:
                    iPublicacao= Publicacao().criarPublicacao(iUsuario)
                    for i in range(len(iVersoes)):
                        Historico().salvaHistorico(iVersoes[i].id_versao, constantes.cntEventoHistoricoPublicar, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
                        Publicacao_Documento().criarPublicacaoDocumento(iPublicacao, iVersoes[i].documento)
                    for i in range(len(iDestinatarios)):
                        Publicacao_Usuario().criarPublicacaoUsuario(iPublicacao, Usuario().obtemUsuarioPeloID(iDestinatarios[i]))
                    
                    iLink = str(settings.PROJECT_ROOT_URL) + 'publicacao/' + str(iPublicacao.id_publicacao)
                    iTexto = iTexto + '<br><br><a href="%(iLink)s" target="_blank">Visualizar Publicado</a><br><br>'% ({'iLink': iLink})
                except Exception, e:
                    oControle.getLogger().error('Nao foi possivel post publicacao email: ' + str(e))
                    return False
                else:
                    if settings.EMAIL:
                        email                   = EmailMessage()
                        email.subject           = iAssunto
                        email.body              = iTexto
                        email.from_email        = iUsuario.email
                        email.content_subtype   = "html"
                        for i in range(len(iDestinatarios)):
                            email.to.append(Usuario().obtemUsuarioPeloID(iDestinatarios[i]).email)
                        email.send()                    
                        for i in range(len(iVersoes)):
                            Historico().salvaHistorico(iVersoes[i].id_versao, constantes.cntEventoHistoricoPublicar, 
                                           iUsuario.id, vRequest.session['IDEmpresa'])
                            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoPublicar, iUsuario.id, 
                                    vRequest.session['IDEmpresa'], vIDVersao=iVersoes[i].id_versao)
                        return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoPublicar) + '/')
            else:
                form = FormEmail(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post email: ' + str(e))
            return False
    else: 
        form = FormEmail(iIDEmpresa=vRequest.session['IDEmpresa'])
        
    return render_to_response(
        'email/publicacao.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )