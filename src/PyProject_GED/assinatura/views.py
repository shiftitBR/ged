# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.http                        import HttpResponseRedirect
from django.conf                        import settings
from django.contrib                     import messages
from django.contrib.auth.decorators     import login_required

from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.documento.models     import Versao
from PyProject_GED                      import oControle, constantes
from PyProject_GED.assinatura.forms     import FormUploadCertificado
from PyProject_GED.assinatura.models    import Certificado, Assinatura
from PyProject_GED.historico.models     import Historico, Log_Usuario
from PyProject_GED.seguranca.models     import Funcao_Grupo

@login_required 
def assinar(vRequest, vTitulo):
    
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
        
    if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoAssinar):
        if vRequest.session['ListaVersao'] != '' and vRequest.session['ListaVersao'] != '-':
            iListaVersao= vRequest.session['ListaVersao'].split('-')[:-1]
            iVersoes= []
            for i in range(len(iListaVersao)):
                iVersao= Versao().obtemVersao(int(iListaVersao[i]))
                if Assinatura().possuiAssinaturaUsuario(iUsuario, iVersao):
                    messages.warning(vRequest, 'O Documento: ' + str(iVersao.documento.assunto) + ' já possui a sua assinatura!' )
                    iPodeAssinar= False
                    break
                else:
                    iPodeAssinar= True
                    iVersoes.append(iVersao)
        else:
            iPodeAssinar   = False
            messages.warning(vRequest, 'Selecione pelo menos 1 (um) documento para executar esta função!')
    else:
        iPodeAssinar    = False
        messages.warning(vRequest, 'Você não possui permissão para executar esta função!')

    if vRequest.POST:
        try :
            form = FormUploadCertificado(vRequest.POST, vRequest.FILES)
            if form.is_valid():
                iSenha       = vRequest.POST.get('senha')
                try:
                    iCertificado = Certificado(arquivo = vRequest.FILES['certificado'])
                    iCertificado.save()
                except:
                    messages.warning(vRequest, 'Senha incorreta ou certificado inválido.' )
                else:
                    iCaminhoCertificado = settings.MEDIA_ROOT + '/' + str(iCertificado.arquivo)
                    iExt         = iCaminhoCertificado.split('.')[1]
                    for i in range(len(iVersoes)):
                        iAssinou = Assinatura().assinaDocumento(iCaminhoCertificado, iSenha, iUsuario, iVersoes[i])
                        if iAssinou:
                            Versao().sinalizaAssinado(iVersoes[i].id_versao)
                            Historico().salvaHistorico(iVersoes[i].id_versao, constantes.cntEventoHistoricoAssinar, 
                                                   iUsuario.id, vRequest.session['IDEmpresa'])
                            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoAssinar, iUsuario.id, 
                                                          vRequest.session['IDEmpresa'], vIDVersao=iVersoes[i].id_versao)
                        else:
                            messages.warning(vRequest, 'Ocorreu um erro ao tentar assinar o documento: ' + iVersoes[i].assunto )
                            break
                    iCertificado.arquivo.delete()
                    iCertificado.delete()
                    if iAssinou :
                        return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoAssinar) + '/')
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post assinar: ' + str(e))
            return False
    else:
        form = FormUploadCertificado()
    
    return render_to_response(
        'assinar/assinar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )