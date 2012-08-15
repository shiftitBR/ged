# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger

from PyProject_GED                      import oControle
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.documento.controle   import Controle as DocumentoControle
from PyProject_GED.documento.models     import Versao
from PyProject_GED.historico.models     import Historico
from forms                              import FormEncaminharPendencia
from models                             import Pendencia
    
import constantes #@UnresolvedImport
from django.http import HttpResponse

@login_required     
def encaminhar(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        
        vIDFuncao = 0
        if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iPossuiPermissao= True
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get encaminhar: ' + str(e))
        return False
    
    if vRequest.POST:
        form = FormEncaminharPendencia(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        if form.is_valid():
            try:
                iDestinatario   = Usuario().obtemUsuarioPeloID(vRequest.POST.get('usr_destinatario'))
                iDescricao      = vRequest.POST.get('descricao')
                iVersao         = Versao().obtemVersao(vIDVersao)
                
                Pendencia().criaPendencia(iUsuario, iDestinatario, iVersao, iDescricao)
                Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoPendente)
                Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoEncaminhar, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel post encaminhar: ' + str(e))
                return False
        else: 
            form = FormEncaminharPendencia(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
    else:
        form = FormEncaminharPendencia(iIDEmpresa=vRequest.session['IDEmpresa'])
        
    return render_to_response(
        'pendencia/encaminhar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required     
def acompanhamento(vRequest, vTitulo):
    try :
        
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        
        iListaDestinatario  = Pendencia().obtemListaPendenciasDestinatario(iUsuario)
        iListaRemetente     = Pendencia().obtemListaPendenciasRemetente(iUsuario)
        
        iPaginator_Remetente = Paginator(iListaRemetente, 10)
        iPaginator_Destinatario = Paginator(iListaDestinatario, 10)
        iPage_Remetente = vRequest.GET.get('page_remetente')
        iPage_Destinatario = vRequest.GET.get('page_destinatario')
        if iPage_Remetente ==None:
            iPage_Remetente = 1
        if iPage_Destinatario ==None:
            iPage_Destinatario = 1
        try:
            iRemetentes = iPaginator_Remetente.page(iPage_Remetente)
        except PageNotAnInteger:
            iRemetentes = iPaginator_Remetente.page(1)
        except EmptyPage:
            iRemetentes = iPaginator_Remetente.page(iPaginator_Remetente.num_pages)
        try:
            iDestinatarios = iPaginator_Destinatario.page(iPage_Destinatario)
        except PageNotAnInteger:
            iDestinatarios = iPaginator_Destinatario.page(1)
        except EmptyPage:
            iDestinatarios = iPaginator_Destinatario.page(iPaginator_Destinatario.num_pages)
        
        vIDFuncao = 0
        if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iPossuiPermissao= True
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get encaminhar: ' + str(e))
        return False
        
    return render_to_response(
        'pendencia/acompanhamento.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )