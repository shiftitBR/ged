# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.conf                        import settings
from django.contrib                     import messages
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.documento.models     import Versao
from controle                           import Controle as AssinaturaControle
from PyProject_GED                      import oControle, constantes
from PyProject_GED.assinatura.forms     import FormUploadCertificado
from PyProject_GED.assinatura.models    import Certificado
from PyProject_GED.historico.models     import Historico, Log_Usuario


def assinar(vRequest, vTitulo):
    
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
        
    iListaVersao= vRequest.session['ListaVersao'].split('-')[:-1]
    iVersoes= []
    for i in range(len(iListaVersao)):
        iVersao= Versao().obtemVersao(int(iListaVersao[i]))
        iVersoes.append(iVersao)
        
    if vRequest.POST:
        try :
            form = FormUploadCertificado(vRequest.POST, vRequest.FILES)
            if form.is_valid():
                iSenha       = vRequest.POST.get('senha')
                iCertificado = Certificado(arquivo = vRequest.FILES['certificado'])
                iCertificado.save()
                iCaminhoCertificado = settings.MEDIA_ROOT + '/' + str(iCertificado.arquivo)
                iExt         = iCaminhoCertificado.split('.')[1]
                for i in range(len(iVersoes)):
                    iCaminhoArquivo = iVersoes[i].upload.image
                    if iExt == 'pfx':
                        iAssinou = AssinaturaControle().assinarPFX(iCaminhoCertificado, iSenha, iCaminhoArquivo)
                    if iAssinou:
                        Historico().salvaHistorico(iVersoes[i].id_versao, constantes.cntEventoHistoricoAssinar, 
                                               iUsuario.id, vRequest.session['IDEmpresa'])
                        Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoAssinar, iUsuario.id, 
                                                      vRequest.session['IDEmpresa'], vIDVersao=iVersoes[i].id_versao)
                    else:
                        messages.warning(vRequest, 'Ocorreu um problema ao assinar ')
                iCertificado.arquivo.delete()
                iCertificado.delete()
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