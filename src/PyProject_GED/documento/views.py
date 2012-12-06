# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.http                        import HttpResponse,\
    HttpResponseRedirect
from django.contrib.auth.decorators     import login_required
from django.contrib                     import messages

from PyProject_GED                      import oControle, constantes
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.historico.models     import Historico, Log_Usuario
from PyProject_GED.seguranca.models     import Pasta, Grupo_Pasta, Funcao_Grupo
from PyProject_GED.workflow.models      import Pendencia
from PyProject_GED.documento.models     import Tipo_de_Documento
from PyProject_GED.indice.models        import Indice_Versao_Valor, Indice_Pasta
from PyProject_GED.ocr.controle         import Controle as ControleOCR
from PyProject_GED.imagem.controle      import Controle as ControleImagem
from controle                           import Controle as DocumentoControle
from models                             import Versao, Documento
from forms                              import FormCheckin, FormUploadDeArquivo
from PyProject_GED.multiuploader.models import MultiuploaderImage
from PyProject_GED.qualidade.models     import Norma, Norma_Documento
from PyProject_GED.assinatura.models    import Assinatura
from django.views.decorators.csrf       import csrf_exempt
from PyProject_GED.envioemail.models    import Email

import datetime
import os
import urllib

@login_required 
def documentos(vRequest, vTitulo):
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
        iEmpresa= Usuario.objects.filter(id= vRequest.user.pk)[0].empresa
        iPasta= Pasta.objects.filter(empresa= iEmpresa.id_empresa).order_by('id_pasta')[0]
        iPasta_Raiz = iEmpresa.pasta_raiz + '/' + str(iPasta.id_pasta) + '/'
        vRequest.session['PastaRaiz']       = iPasta_Raiz
        vRequest.session['IDEmpresa']       = iUsuario.empresa.id_empresa
        vRequest.session['ListaVersao']     = ''
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get documentos: ' + str(e))
            return False
    return render_to_response(
        'documentos/documentos.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )

@login_required 
def obtemPastaRaiz(vRequest, vTitulo):
    try :
        iEmpresa= Usuario.objects.filter(id= vRequest.user.pk)[0].empresa
        iPasta= Pasta.objects.filter(empresa= iEmpresa.id_empresa).order_by('id_pasta')[0]
        iPasta_Raiz = iEmpresa.pasta_raiz + '/' + str(iPasta.id_pasta) + '/'
        iHtml= []
        iHtml.append(iPasta_Raiz)
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel obter pasta raiz: ' + str(e))
        return False
    return HttpResponse(''.join(iHtml))

@login_required 
def versoesSelecionadas(vRequest, vTitulo, vListaIDVersoes):
    try :
        vRequest.session['ListaVersao']= vListaIDVersoes
        return HttpResponse(True)
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel obter pasta raiz: ' + str(e))
        return False


@login_required 
def tabelaDocumentos(vRequest, vTitulo):
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
        iPasta_Raiz = vRequest.session['IDPasta'] #Variavel utilizado na interface
        iListaDocumentos=[]
        if vRequest.session['IDPasta'] != '':
            iListaDocumentos = Versao().obtemListaDeDocumentosDaPasta(vRequest.session['IDEmpresa'], vRequest.session['IDPasta'])
            vRequest.session['iListaDocumento']= iListaDocumentos
            iHtml= []
            if len(iListaDocumentos) > 0:
                for i in range(len(iListaDocumentos)):  
                    iEstado = iListaDocumentos[i].id_estado 
                    if iListaDocumentos[i].assinado:
                        iAssinado = '<i class="icon-pencil">'
                    else:
                        iAssinado = ' '
                    iPodeCheckIn = Historico().verificaUsuarioAcao(iUsuario.id, constantes.cntEventoHistoricoCheckout, iListaDocumentos[i].id_versao) 
                    iLinha= '<tr><td><label class="checkbox"><input type="checkbox" name="versao_%(iIDVersao)s" value="option1"></label></td><td><center>%(iProtocolo)s</center></td><td>%(iAssunto)s</td><td>%(iTipo)s</td><td>%(iEstado)s</td><td>%(iUsuario)s</td><td><center>%(iVersao)s</center></td><td><center>%(iData)s</center></td><td><center>%(iAssinado)s</center></td><td>' % (
                              {'iVersao': str(iListaDocumentos[i].num_versao), 
                               'iIDVersao': str(iListaDocumentos[i].id_versao),
                               'iProtocolo': str(iListaDocumentos[i].protocolo), 
                               'iAssunto': str(iListaDocumentos[i].assunto),
                               'iTipo': str(iListaDocumentos[i].tipo_documento), 
                               'iEstado': str(iListaDocumentos[i].estado), 
                               'iUsuario': str(iListaDocumentos[i].criador), 
                               'iData': str(iListaDocumentos[i].data_criacao),
                               'iAssinado': str(iAssinado)})
                    
                    iLinha= iLinha + '<div class="btn-group">'
                    if iEstado == constantes.cntEstadoVersaoExcluida:
                        iLinha= iLinha + '<a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#"><i class="icon-plus-sign icon-white"></i> Informações   <span class="caret"></span></a><ul class="dropdown-menu">'
                    else:
                        if iListaDocumentos[i].tipoVisualizacao == constantes.cntTipoVisualizacaoPDF:
                            iLinha= iLinha + '<a class="btn btn-primary" href="%(iArquivo)s" target="_blank" title="%(iAssunto)s"><i class="icon-camera icon-white"></i> Visualizar</a>'% ({'iArquivo': str(iListaDocumentos[i].caminhoVisualizar), 'iAssunto': str(iListaDocumentos[i].assunto)})    
                        elif iListaDocumentos[i].tipoVisualizacao == constantes.cntTipoVisualizacaoImagem:
                            iLinha= iLinha + '<a class="btn btn-primary fancybox fancybox.iframe" href="/visualizar/%(iIDVersao)s/"><i class="icon-camera icon-white"></i> Visualizar</a>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        elif iListaDocumentos[i].tipoVisualizacao == constantes.cntTipoVisualizacaoOutro:
                            iLinha= iLinha + '<a class="btn btn-primary" href="/download/%(iIDVersao)s/"><i class="icon-download-alt icon-white"></i>  Download</a>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        iLinha= iLinha + '<button class="btn btn-primary dropdown-toggle" data-toggle="dropdown"><span class="caret"></span></button><ul class="dropdown-menu">'
                        
                    iEstado = iListaDocumentos[i].id_estado
                    
                    if iListaDocumentos[i].tipoVisualizacao == constantes.cntTipoVisualizacaoPDF or iListaDocumentos[i].tipoVisualizacao == constantes.cntTipoVisualizacaoImagem:
                        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoDownload):
                            iLinha= iLinha + '<li><a href="/download/%(iIDVersao)s/"><i class="icon-download-alt"></i>  Download</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        else:
                            iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/download/0/"><i class="icon-download-alt"></i>  Download</a></li>'
                    if iListaDocumentos[i].ehImagemExportavel:
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/tipo_exportar/%(iIDVersao)s/"><i class="icon-arrow-up"></i>  Exportar</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        
                    if iEstado == constantes.cntEstadoVersaoDisponivel or iEstado == constantes.cntEstadoVersaoAprovado or iEstado == constantes.cntEstadoVersaoReprovado: #CheckOut
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/checkout/%(iIDVersao)s/"><i class="icon-edit"></i>  Check-out</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        
                    if iEstado == constantes.cntEstadoVersaoDisponivel : #Encaminhar
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/tipo_pendencia/%(iIDVersao)s/"><i class="icon-share-alt"></i>  Encaminhar</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})   
                        
                    if iEstado == constantes.cntEstadoVersaoBloqueado  and iPodeCheckIn: #CheckIn
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/checkin/%(iIDVersao)s/"><i class="icon-share"></i>  Check-in</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        
                    if iEstado == constantes.cntEstadoVersaoDisponivel : #Excluir
                        iLinha= iLinha + '<li class="divider"></li>'
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/excluir_documento/%(iIDVersao)s/"><i class="icon-trash"></i>  Excluir</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        
                    iLinha= iLinha + '<li class="divider"></li><li><a class="fancybox fancybox.iframe" href="/historico/%(iIDVersao)s/"><i class="icon-book"></i>  Histórico</a></li></ul></div></td></tr>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                    iHtml.append(iLinha)
            return HttpResponse(''.join(iHtml))
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tabela documentos: ' + str(e))
            return False

@login_required     
def importar(vRequest, vTitulo):
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
            
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoImportar):
            if not Pasta().ehPastaRaiz(vRequest.session['IDPasta'], vRequest.session['IDEmpresa']):
                iListaTipoDocumento = Tipo_de_Documento().obtemListaTipoDocumentoDaEmpresa(vRequest.session['IDEmpresa'])
                iListaIndices       = Indice_Pasta().obtemIndicesDaPasta(vRequest.session['IDPasta'])
                iTamListaIndices    = len(iListaIndices)
                iListaUsuarios      = Usuario.objects.filter(empresa= iUsuario.empresa.id_empresa)
                iListaNomes         = DocumentoControle().obtemListaNomesUsuarios(iListaUsuarios)
                iPossuiPermissao    = True
            else:
                messages.warning(vRequest, 'Selecione uma Pasta para Inserir Documento!')
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.')
        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get importar: ' + str(e))
            return False
    
    if vRequest.POST:
        form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        if form.is_valid():
            try:
                iListaImages= MultiuploaderImage().obtemListaDeUploadsDoUsuario(vRequest.user, vRequest.session['IDGrupo_Upload'])
                if iListaImages == True or not iListaImages == None:
                    #Adicionar na tabela documeto e versao
                    if len(vRequest.POST.get('data_validade')) != 10:
                        iDataValidade= None
                    else:
                        iListaDataValidade= vRequest.POST.get('data_validade').split('/')
                        iDataValidade= datetime.datetime(int(iListaDataValidade[2]), int(iListaDataValidade[1]), int(iListaDataValidade[0]), 00, 00, 00)
                    if len(vRequest.POST.get('data_descarte')) != 10:
                        iDataDescarte= None
                    else:
                        iListaDataDescarte= vRequest.POST.get('data_descarte').split('/')
                        iDataDescarte= datetime.datetime(int(iListaDataDescarte[2]), int(iListaDataDescarte[1]), int(iListaDataDescarte[0]), 00, 00, 00)
                    iAssunto    = vRequest.POST.get('assunto')
                    iIDResponsavel= vRequest.POST.get('usr_responsavel')
                    iResponsavel= Usuario().obtemUsuarioPeloID(iIDResponsavel)
                    if vRequest.POST.get('eh_publico') != None:
                        iEh_Publico = True
                    else:
                        iEh_Publico = False
                    iIDTipo_Documento = vRequest.POST.get('tipo_documento')
                    
                    iCount=0
                    for iImage in iListaImages:
                        iCount= iCount + 1
                        if len(iListaImages) > 1:
                            iAssuntoLote= '%s - %02d' % (iAssunto, iCount)
                        else:
                            iAssuntoLote= iAssunto
                        iDocumento  = Documento().salvaDocumento(vRequest.session['IDEmpresa'], iIDTipo_Documento, vRequest.session['IDPasta'], 
                                                                 iAssuntoLote, iEh_Publico, iResponsavel, iDataValidade, iDataDescarte)
                        iProtocolo  = Documento().gerarProtocolo(iDocumento.id_documento, 1) 
                        iVersao     = Versao().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                                        1, 1, iImage.key_data, iProtocolo)
                        #Associar Normas
                        iNormas = vRequest.POST.getlist('norma')
                        for i in range(len(iNormas)):
                            iNorma = Norma().obtemNorma(iNormas[i])
                            Norma_Documento().criaNorma_Documento(iNorma, iDocumento)
                        #Salvar Indices
                        for i in range(len(iListaIndices)):
                            iIndice = iListaIndices[i]
                            iValor  = vRequest.POST.get('indice_%s' % iIndice.id_indice)
                            if iValor != '':
                                Indice_Versao_Valor().salvaValorIndice(iValor, iIndice.id_indice, iVersao.id_versao)
                        ControleOCR().executaOCR(iVersao)
                        ControleImagem().comprimeImagem(iVersao)
                        Pendencia().criaPendenciasDoWorkflow(iDocumento)
                        Historico().salvaHistorico(iVersao.id_versao, constantes.cntEventoHistoricoImportar, 
                                                   iUsuario.id, vRequest.session['IDEmpresa'])
                        Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoImportar, iUsuario.id, 
                                                  vRequest.session['IDEmpresa'], vIDVersao=iVersao.id_versao)
                    return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoImportar) + '/')
                else:
                    messages.warning(vRequest, 'Faça o Upload de 1 (um) documento para executar esta função!')
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel importar: ' + str(e))
                messages.warning(vRequest, 'Não foi possível importar o(s) arquivo(s) solicitados!')
                return HttpResponseRedirect('/importar/')
        else:
            form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
    else: 
        form = FormUploadDeArquivo(iIDEmpresa=vRequest.session['IDEmpresa'])
        vRequest.session['IDGrupo_Upload']= MultiuploaderImage().obtemGrupoDeUpload()
                                           
    return render_to_response(
        'acao/importar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )

@login_required     
def checkin(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario    = Usuario().obtemUsuario(vRequest.user)
        iVersao = Versao().obtemVersao(vIDVersao)
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoCheckinChekout):
            if DocumentoControle().podeExecutarFuncao(iVersao.estado.id_estado_da_versao, 
                                                      constantes.cntEstadoVersaoObsoleto):
                iVersaoBase = Versao().obtemVersao(vIDVersao)
                iDocumento  = iVersaoBase.documento
                vIDFuncao = 0
                iPossuiPermissao= True
            else:
                messages.warning(vRequest, 'Não é possível fazer o Check-in do Documento!') 
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.')
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get checkin: ' + str(e))
        return False
    
    if vRequest.POST:
        form = FormCheckin(vRequest.POST)
        if form.is_valid():
            try:
                iListaImages= MultiuploaderImage().obtemListaDeUploadsDoUsuario(vRequest.user, vRequest.session['IDGrupo_Upload'])
                if iListaImages == True or not iListaImages == None:
                    iImage      = iListaImages[0]
                    iDescricao  = vRequest.POST.get('descricao')
                    iProtocolo  = Documento().gerarProtocolo(iDocumento.id_documento, int(iVersaoBase.versao)+1)
                    iVersao     = Versao().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                                        1, int(iVersaoBase.versao)+1, iImage.key_data, iProtocolo, 
                                                        vDsc_Modificacao=iDescricao)
                    Versao().obsoletarVersao(iVersaoBase)
                    Historico().salvaHistorico(iVersaoBase.id_versao, constantes.cntEventoHistoricoObsoletar, 
                                           iUsuario.id, vRequest.session['IDEmpresa'])
                    Historico().salvaHistorico(iVersao.id_versao, constantes.cntEventoHistoricoCheckIn, 
                                           iUsuario.id, vRequest.session['IDEmpresa'])
                    Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoCheckIn, iUsuario.id, 
                                                  vRequest.session['IDEmpresa'], vIDVersao=iVersao.id_versao)
                    vRequest.session['Images']= False
                    ControleOCR().executaOCR(iVersao)
                    ControleImagem().comprimeImagem(iVersao)
                    Pendencia().criaPendenciasDoWorkflow(iDocumento)
                    return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoCheckinChekout) + '/')
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel post checkin: ' + str(e))
                return False
        else:
            form = FormCheckin(vRequest.POST)
            iErro= True
    else: 
        form = FormCheckin()
        vRequest.session['IDGrupo_Upload']= MultiuploaderImage().obtemGrupoDeUpload()
                                           
    return render_to_response(
        'documentos/checkin.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def checkout(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        iVersao = Versao().obtemVersao(vIDVersao)
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoCheckinChekout):
            if DocumentoControle().podeExecutarFuncao(iVersao.estado.id_estado_da_versao, 
                                                      constantes.cntEstadoVersaoBloqueado):
                vIDFuncao = 0
                iPossuiPermissao= True
            else:
                messages.warning(vRequest, 'Não é possível fazer o Check-out do Documento!') 
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.')    
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get checkout: ' + str(e))
        return False
        
    if vRequest.POST:
        try :
            if DocumentoControle().podeExecutarFuncao(iVersao.estado.id_estado_da_versao, 
                                                      constantes.cntEstadoVersaoBloqueado):
                Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoBloqueado)
                Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoCheckout, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
                Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoCheckout, iUsuario.id, 
                                              vRequest.session['IDEmpresa'], vIDVersao=vIDVersao)
                iArquivo= str(Versao().obtemCaminhoArquivo(vIDVersao))
                iFile = open(iArquivo,"r")
                response = HttpResponse(iFile.read())
                response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iArquivo)[1]
                return response
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post checkout: ' + str(e))
            return False
    return render_to_response(
        'documentos/checkout.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def aprovar(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        iVersao = Versao().obtemVersao(vIDVersao)
        if DocumentoControle().podeExecutarFuncao(iVersao.estado.id_estado_da_versao, 
                                                      constantes.cntEstadoVersaoReprovado):
            vIDFuncao = 0
            iPossuiPermissao= True
        else:
            messages.warning(vRequest, 'Este Documento não pode ser aprovado!') 
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get aprovar: ' + str(e))
        return False
    
    if vRequest.POST:
        try :
            if vRequest.POST.get('comentario') != '' :
                iVersao = Versao().obtemVersao(vIDVersao)
                iPendencia = Pendencia().obtemPendencia(iVersao, iUsuario)
                Pendencia().trataPendencia(iVersao.documento, constantes.cntAcaoPendenciaAprovar, 
                                           iUsuario, vRequest.POST.get('comentario'))
                Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoAprovar, iUsuario.id, 
                                        vRequest.session['IDEmpresa'], vIDVersao=vIDVersao)
                Email().enviaEmailPorTipo(constantes.cntConfiguracaoEmailAlerta, iPendencia.usr_remetente.email, 
                                          constantes.cntTipoEmailPendenciaAprovada)
                return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoAprovarReprovar) + '/')
            else:
                messages.success(vRequest, 'Adicione um Comentário para Aprovar o Documento!.') 
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post aprovar: ' + str(e))
            return False
    return render_to_response(
        'acao/aprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def reprovar(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        iVersao = Versao().obtemVersao(vIDVersao)
        if DocumentoControle().podeExecutarFuncao(iVersao.estado.id_estado_da_versao, 
                                                      constantes.cntEstadoVersaoReprovado):
            vIDFuncao = 0
            iPossuiPermissao= True
        else:
            messages.warning(vRequest, 'Este Documento não pode ser reprovado!') 
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get reprovar: ' + str(e))
        return False
    
    if vRequest.POST:
        try :
            if vRequest.POST.get('comentario') != '' :
                iVersao = Versao().obtemVersao(vIDVersao)
                iPendencia = Pendencia().obtemPendencia(iVersao, iUsuario)
                Pendencia().trataPendencia(iVersao.documento, constantes.cntAcaoPendenciaReprovar, 
                                           iUsuario, vRequest.POST.get('comentario'))
                Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoReprovar, iUsuario.id, 
                                        vRequest.session['IDEmpresa'], vIDVersao=vIDVersao)
                Email().enviaEmailPorTipo(constantes.cntConfiguracaoEmailAlerta, iPendencia.usr_remetente.email, 
                                          constantes.cntTipoEmailPendenciaReprovada)
                return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoAprovarReprovar) + '/')
            else:
                messages.success(vRequest, 'Adicione um Comentário para Reprovar o Documento!.')
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post reprovar: ' + str(e))
            return False
    return render_to_response(
        'acao/reprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def excluir(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        iVersao = Versao().obtemVersao(vIDVersao)
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoExcluir):
            if DocumentoControle().podeExecutarFuncao(iVersao.estado.id_estado_da_versao, 
                                                      constantes.cntEstadoVersaoExcluida):
                vIDFuncao = 0
                iPossuiPermissao= True
            else:
                messages.warning(vRequest, 'Este Documento não pode ser excluido!') 
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.') 
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get excluir: ' + str(e))
        return False
    
    if vRequest.POST:
        try :
            Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoExcluida)
            Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoExcluir, 
                                   iUsuario.id, vRequest.session['IDEmpresa'])
            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoExcluir, iUsuario.id, 
                                    vRequest.session['IDEmpresa'], vIDVersao=vIDVersao)
            return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoExcluir) + '/')
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post excluir: ' + str(e))
            return False
    return render_to_response(
        'acao/excluir.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )


def download(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        iVersao = Versao().obtemVersao(vIDVersao)
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoDownload):
            vIDFuncao = 0
            iArquivo = str(Versao().obtemCaminhoArquivo(vIDVersao))
            if iVersao.eh_assinado:
                iListaAssinaturas = Assinatura().obtemListaAssDaVersao(iVersao)
                iArquivo= DocumentoControle().comprimiArquivoAssinado(iVersao, iListaAssinaturas)
            else:
                iArquivo= iArquivo
            Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoDownload, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoDownload, iUsuario.id, 
                                    vRequest.session['IDEmpresa'], vIDVersao=vIDVersao)
            iPossuiPermissao= True
            iFile = open(iArquivo,"r")
            iResponseP7s = HttpResponse(iFile.read())
            iResponseP7s["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iArquivo)[1]
            return iResponseP7s
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.') 
        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel fazer download do arquivo: ' + str(e))
            return False
    return render_to_response(
        'acao/download.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def criaArvore(vRequest, vTitulo):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        iDiretorio=urllib.unquote(vRequest.POST.get('dir',''))
        vRequest.session['Diretorio_Pasta'] = iDiretorio
        vRequest.session['IDPasta'] = DocumentoControle().obtemIDPastaArvore(iDiretorio)
        iListaDocumentos = Versao().obtemListaDeDocumentosDaPasta(vRequest.session['IDEmpresa'], vRequest.session['IDPasta'])
        try:
            iHtml=['<ul class="jqueryFileTree" style="display: none;">']
            for iPasta in os.listdir(iDiretorio):
                iDiretorioFilho=os.path.join(iDiretorio, iPasta)
                if os.path.isdir(iDiretorioFilho):
                    if 'temp' not in iDiretorioFilho:
                        iNomePasta= Pasta().obtemNomeDaPasta(iPasta)
                        if Grupo_Pasta().possuiAcessoPasta(iUsuario, iPasta):
                            iHtml.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (iDiretorioFilho, iNomePasta))
            iHtml.append('</ul>')
        except Exception,e:
            iHtml.append('Nao foi possivel carregar o diretorio: %s' % str(e))
        iHtml.append('</ul>')
        return HttpResponse(''.join(iHtml))
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel criar arvore: ' + str(e))
            return False

def visualizar(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoVisualizar):
            iVersao     = Versao().obtemVersao(vIDVersao)
            iImagem     = Versao().obtemDocumentoAuxiliar(iVersao).caminhoVisualizar
            iDiretorioImagemTemporaria= ControleImagem().criaImagemTemporaria(iVersao, iUsuario.id)
            vRequest.session['Imagem_Temporaria']= iDiretorioImagemTemporaria
            Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoVisualizar, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoVisualizar, iUsuario.id, 
                                    vRequest.session['IDEmpresa'], vIDVersao=vIDVersao)
            iPossuiPermissao= True
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.') 
        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel fazer visualizar o arquivo: ' + str(e))
            return False

    return render_to_response(
        'acao/visualizar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )       

@csrf_exempt
def digitalizar(vRequest):
    print '>>>>>>>>>>>>>>>>>>. digitalizar'
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoDigitalizar):
            if not Pasta().ehPastaRaiz(vRequest.session['IDPasta'], vRequest.session['IDEmpresa']):
                iListaIndices       = Indice_Pasta().obtemIndicesDaPasta(vRequest.session['IDPasta'])
                iPossuiPermissao    = True
            else:
                messages.warning(vRequest, 'Selecione uma Pasta para Digitalizar Documento!')
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.')
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get digitalizar: ' + str(e))
            return False
    
    if vRequest.method == 'POST':
        form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        if form.is_valid():
            try:
                iListaImages= MultiuploaderImage().obtemListaDeUploadsDoUsuario(vRequest.user, vRequest.session['IDGrupo_Upload'])
                if iListaImages == True or not iListaImages == None:
                    #Adicionar na tabela documeto e versao
                    if len(vRequest.POST.get('data_validade')) != 10:
                        iDataValidade= None
                    else:
                        iListaDataValidade= vRequest.POST.get('data_validade').split('/')
                        iDataValidade= datetime.datetime(int(iListaDataValidade[2]), int(iListaDataValidade[1]), int(iListaDataValidade[0]), 00, 00, 00)
                    if len(vRequest.POST.get('data_descarte')) != 10:
                        iDataDescarte= None
                    else:
                        iListaDataDescarte= vRequest.POST.get('data_descarte').split('/')
                        iDataDescarte= datetime.datetime(int(iListaDataDescarte[2]), int(iListaDataDescarte[1]), int(iListaDataDescarte[0]), 00, 00, 00)
                    iAssunto    = vRequest.POST.get('assunto')
                    iIDResponsavel= vRequest.POST.get('usr_responsavel')
                    iResponsavel= Usuario().obtemUsuarioPeloID(iIDResponsavel)
                    if vRequest.POST.get('eh_publico') != None:
                        iEh_Publico = True
                    else:
                        iEh_Publico = False
                    iIDTipo_Documento = vRequest.POST.get('tipo_documento')
                    
                    iCount=0
                    for iImage in iListaImages:
                        iCount= iCount + 1
                        if len(iListaImages) > 1:
                            iAssuntoLote= '%s - %02d' % (iAssunto, iCount)
                        else:
                            iAssuntoLote= iAssunto
                        iDocumento  = Documento().salvaDocumento(vRequest.session['IDEmpresa'], iIDTipo_Documento, vRequest.session['IDPasta'], 
                                                                 iAssuntoLote, iEh_Publico, iResponsavel, iDataValidade, iDataDescarte)
                        iProtocolo  = Documento().gerarProtocolo(iDocumento.id_documento, 1) 
                        iVersao     = Versao().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                                        1, 1, iImage.key_data, iProtocolo)
                        #Associar Normas
                        iNormas = vRequest.POST.getlist('norma')
                        for i in range(len(iNormas)):
                            iNorma = Norma().obtemNorma(iNormas[i])
                            Norma_Documento().criaNorma_Documento(iNorma, iDocumento)
                        #Salvar Indices
                        for i in range(len(iListaIndices)):
                            iIndice = iListaIndices[i]
                            iValor  = vRequest.POST.get('indice_%s' % iIndice.id_indice)
                            if iValor != '':
                                Indice_Versao_Valor().salvaValorIndice(iValor, iIndice.id_indice, iVersao.id_versao)
                        ControleOCR().executaOCR(iVersao)
                        ControleImagem().comprimeImagem(iVersao)
                        Pendencia().criaPendenciasDoWorkflow(iDocumento)
                        Historico().salvaHistorico(iVersao.id_versao, constantes.cntEventoHistoricoImportar, 
                                                   iUsuario.id, vRequest.session['IDEmpresa'])
                        Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoImportar, iUsuario.id, 
                                                  vRequest.session['IDEmpresa'], vIDVersao=iVersao.id_versao)
                    return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoImportar) + '/')
                else:
                    messages.warning(vRequest, 'Faça o Upload de 1 (um) documento para executar esta função!')
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel digitalizar: ' + str(e))
                messages.warning(vRequest, 'Não foi possível importar o(s) arquivo(s) solicitados!')
                return HttpResponseRedirect('/digitalizar/')
        else:
            form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
    else: 
        form = FormUploadDeArquivo(iIDEmpresa=vRequest.session['IDEmpresa'])
        grupoID= MultiuploaderImage().obtemGrupoDeUpload()
        empresaID= vRequest.session['IDEmpresa']
        pastaID= vRequest.session['IDPasta']
        vRequest.session['IDGrupo_Upload']= MultiuploaderImage().obtemGrupoDeUpload()
    return render_to_response(
        'acao/digitalizar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )    