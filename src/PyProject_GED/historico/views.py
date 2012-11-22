# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib                     import messages

from models                             import Historico
from PyProject_GED.documento.models     import Versao
from PyProject_GED.documento.models     import Documento
from PyProject_GED.seguranca.models     import Funcao_Grupo
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED                      import constantes
from PyProject_GED.assinatura.models import Assinatura


def historico(vRequest, vTitulo, vIDVersao=None):
    iUser = vRequest.user
    if iUser:
        iUsuario= Usuario().obtemUsuario(iUser)
    
    if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoHistorico):
        iVersao         = Versao().obtemVersao(vIDVersao)
        iDocumento      = Documento().obtemInformacoesDocumento(vIDVersao)
        if iDocumento.dataDescarte == None:
            iDocumento.dataDescarte= 'Não informado'
        if iDocumento.dataValidade == None:
            iDocumento.dataValidade= 'Não informado'
        iListaVersao    = Versao().obtemListaDeVersoesDoDocumento(vIDVersao)
        iListaEventos   = Historico().obtemListaEventos(vIDVersao)
        iUltimaVersao   = iListaVersao[len(iListaVersao)-1].num_versao
        iAssinatuas     = Assinatura().obtemListaInfoAss(iVersao)
        iPossuiPermissao= True
    else:
        messages.warning(vRequest, 'Você não possui permissão para executar esta função.')
    
    return render_to_response(
        'historico/historico.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )