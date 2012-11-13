# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger
from django.contrib                     import messages
from django.http                        import HttpResponseRedirect, HttpResponse

from PyProject_GED                      import oControle, constantes
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.documento.controle   import Controle as DocumentoControle
from PyProject_GED.documento.models     import Versao
from PyProject_GED.historico.models     import Log_Usuario
from PyProject_GED.seguranca.models     import Funcao_Grupo
from PyProject_GED.workflow.models      import Tipo_de_Pendencia
from forms                              import FormEncaminharPendencia
from models                             import Pendencia
from PyProject_GED.envioemail.models import Email
    

@login_required     
def encaminhar(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        iVersao = Versao().obtemVersao(vIDVersao)
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoEncaminhar):
            if DocumentoControle().podeExecutarFuncao(iVersao.estado.id_estado_da_versao, 
                                                      constantes.cntEstadoVersaoExcluida):
                vIDFuncao = 0
                iPossuiPermissao= True
            else:
                messages.warning(vRequest, 'Este Documento não pode ser Encaminhado!') 
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.')
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get encaminhar: ' + str(e))
        return False
    
    if vRequest.POST:
        form = FormEncaminharPendencia(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'], iIDTipoPendencia=vRequest.session['TipoPendencia'])
        if form.is_valid():
            try:
                iDescricao      = vRequest.POST.get('descricao')
                iVersao         = Versao().obtemVersao(vIDVersao)
                iUsuarios       = vRequest.POST.getlist('usr_destinatario')
                if vRequest.POST.get('eh_multipla') != None:
                    iMultipla = True
                else:
                    iMultipla = False
                iListaDestinatarios= []
                for iUser in iUsuarios:
                    iListaDestinatarios.append(Usuario().obtemUsuarioPeloID(iUser))
                iTipoPendencia  = Tipo_de_Pendencia.objects.filter(id_tipo_de_pendencia=vRequest.session['TipoPendencia'])[0]
                Pendencia().criaPendencia(iUsuario, iListaDestinatarios, iVersao, 
                                          iDescricao, iTipoPendencia, vEhMultipla=iMultipla)
                Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoEncaminhar, iUsuario.id, 
                                    vRequest.session['IDEmpresa'], vIDVersao=vIDVersao)
                for iDestinatario in iListaDestinatarios:
                    Email().enviaEmailPorTipo(constantes.cntConfiguracaoEmailAlerta, iDestinatario.email, 
                                              constantes.cntTipoEmailPendenciaRecebida)
                return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoEncaminhar) + '/')
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel post encaminhar: ' + str(e))
                return False
        else: 
            form = FormEncaminharPendencia(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'], iIDTipoPendencia=vRequest.session['TipoPendencia'])
    else:
        form = FormEncaminharPendencia(iIDEmpresa=vRequest.session['IDEmpresa'], iIDTipoPendencia=vRequest.session['TipoPendencia'])
        
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
    
@login_required     
def tipo_pendencia(vRequest, vTitulo, vIDVersao=None):
    
    iUsuario= Usuario().obtemUsuario(vRequest.user)
        
    if vRequest.POST:
        try :
            vRequest.session['TipoPendencia'] = vRequest.POST.get('tipo_pendencia')
            return HttpResponseRedirect('/encaminhar/%s/' % vIDVersao)
        
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post tipo_pendencia: ' + str(e))
        return False
        
    return render_to_response(
        'pendencia/tipo_pendencia.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
        
@login_required 
def obtemQuantidadeDePendencias(vRequest, vTitulo):
    try :
        if vRequest.user != None :
            iQuantidade= Pendencia().obtemQuantidadePendenciasDestinatario(vRequest.user.id)
            iHtml= []
            iHtml.append(str(iQuantidade))
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel obter a quantidade de Pendencias: ' + str(e))
        return False
    return HttpResponse(''.join(iHtml))