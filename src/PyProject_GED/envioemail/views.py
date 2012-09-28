# -*- coding: utf-8 -*- 
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.core.mail                   import EmailMessage
from django.conf                        import settings
from django.contrib                     import messages
from django.http                        import HttpResponseRedirect

from PyProject_GED.documento.models     import Versao
from PyProject_GED.autenticacao.models  import Usuario, Empresa
from PyProject_GED.envioemail.forms     import FormEmail
from PyProject_GED                      import oControle, constantes
from objetos_auxiliares                 import Destinatario
from PyProject_GED.historico.models     import Historico, Log_Usuario
from PyProject_GED.envioemail.models    import Publicacao, Publicacao_Documento, Publicacao_Usuario
from PyProject_GED.documento.controle   import Controle as DocumentoControle
from PyProject_GED.seguranca.models     import Funcao_Grupo
from PyProject_GED.assinatura.models    import Assinatura

def email(vRequest, vTitulo):  
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
        
    if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoEmail):
        if vRequest.session['ListaVersao'] != '' and vRequest.session['ListaVersao'] != '-':
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
            iCadastraContato= Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoCadastrarContato)
            iPossuiPermissao    = True
        else:
            messages.warning(vRequest, 'Selecione pelo menos 1 (um) documento para executar esta função!')
    else:
        messages.warning(vRequest, 'Você não possui permissão para executar esta função!')

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
                                iListaAssinaturas = Assinatura().obtemListaAssDaVersao(iVersoes[i])
                                iFileAnexo  = DocumentoControle().comprimiArquivoAssinado(iVersoes[i], iListaAssinaturas)
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
                        vRequest.session['ListaVersao'] = ''
                        return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoEmail) + '/')
                except Exception, e:
                    oControle.getLogger().error('Nao foi possivel post email: ' + str(e))
                    return False
                else:
                    form = FormEmail(iIDEmpresa=vRequest.session['IDEmpresa'])
            else:
                form = FormEmail(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        except Exception, e:
            vRequest.session['ListaVersao'] = ''
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
        
    if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoPublicar):
        if vRequest.session['ListaVersao'] != '' and vRequest.session['ListaVersao'] != '-':
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
            iCadastraContato= Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoCadastrarContato)
            iPossuiPermissao    = True
        else:
            messages.warning(vRequest, 'Selecione pelo menos 1 (um) documento para executar esta função!')
    else:
        messages.warning(vRequest, 'Você não possui permissão para executar esta função!')
        
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
                        vRequest.session['ListaVersao'] = ''
                        return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoPublicar) + '/')
            else:
                form = FormEmail(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        except Exception, e:
            vRequest.session['ListaVersao'] = ''
            oControle.getLogger().error('Nao foi possivel post email: ' + str(e))
            return False
    else: 
        form = FormEmail(iIDEmpresa=vRequest.session['IDEmpresa'])
        
    return render_to_response(
        'email/publicacao.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )