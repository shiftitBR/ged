# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.http                        import HttpResponse
from django.contrib.auth.decorators     import login_required

from PyProject_GED                      import oControle
from PyProject_GED.autenticacao.models  import Usuario
from controle                           import Controle as DocumentoControle
from models                             import Versao
from PyProject_GED.historico.models     import Historico
from PyProject_GED.seguranca.models     import Pasta
from PyProject_GED.workflow.models      import Pendencia
from forms                              import FormCheckin

import os
import urllib
import constantes #@UnresolvedImport

@login_required 
def documentos(vRequest, vTitulo):
    try :
        iEmpresa= Usuario.objects.filter(id= vRequest.user.pk)[0].empresa
        vRequest.session['IDEmpresa'] = iEmpresa.id_empresa
        iPasta= Pasta.objects.filter(empresa= iEmpresa.id_empresa).order_by('id_pasta')[0]
        iPasta_Raiz = iEmpresa.pasta_raiz + '/' + str(iPasta.id_pasta) + '/'
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get documentos: ' + str(e))
            return False
        
    if vRequest.POST:
        try :
            iListaCheck=[]
            iListaVersao = ''
            iListaDocumentos= vRequest.session['iListaDocumento']
            for i in range(len(iListaDocumentos)): 
                if 'versao_%s' % iListaDocumentos[i].id_versao in vRequest.POST:
                    iListaCheck.append(iListaDocumentos[i].id_versao)
                    iListaVersao = str(iListaDocumentos[i].id_versao) + iListaVersao
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post documentos: ' + str(e))
            return False
    return render_to_response(
        'documentos/documentos.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def tabelaDocumentos(vRequest, vTitulo):
    try :
        iPasta_Raiz = vRequest.session['IDPasta']
        iListaDocumentos=[]
        if vRequest.session['IDPasta'] != '':
            iListaDocumentos = Versao().obtemListaDeDocumentosDaPasta(vRequest.session['IDEmpresa'], vRequest.session['IDPasta'])
            vRequest.session['iListaDocumento']= iListaDocumentos
            iHtml= []
            if len(iListaDocumentos) > 0:
                for i in range(len(iListaDocumentos)):     
                    iLinha= '<tr><td><label class="checkbox"><input type="checkbox" name="versao_%(iIDVersao)s" value="option1"></label></td><td><center>%(iProtocolo)s</center></td><td>%(iAssunto)s</td><td>%(iTipo)s</td><td>%(iEstado)s</td><td>%(iUsuario)s</td><td><center>%(iVersao)s</center></td><td><center>%(iData)s</center></td><td><div class="btn-group">' % (
                              {'iVersao': str(iListaDocumentos[i].num_versao), 
                               'iIDVersao': str(iListaDocumentos[i].id_versao),
                               'iProtocolo': str(iListaDocumentos[i].protocolo), 
                               'iAssunto': str(iListaDocumentos[i].assunto),
                               'iTipo': str(iListaDocumentos[i].tipo_documento), 
                               'iEstado': str(iListaDocumentos[i].estado), 
                               'iUsuario': str(iListaDocumentos[i].criador), 
                               'iData': str(iListaDocumentos[i].data_criacao)})
                    #iLinha= iLinha + '<a class="btn btn-primary" href="%(iArquivo)s" data-fancybox-group="gallery" title="%(iAssunto)s"><i class="icon-camera icon-white"></i> Visualizar</a>'% ({'iArquivo': str(iListaDocumentos[i].caminhoVisualizar), 'iAssunto': str(iListaDocumentos[i].assunto)})
                    # iLinha= iLinha + '<a class="btn btn-primary" href="/visualizar/%(iIDVersao)s/"><i class="icon-camera icon-white"></i>  Visualizar</a>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                    #if iListaDocumentos[i].visualizavel :
                    #    iLinha= iLinha + '<a class="btn btn-primary" href="%(iArquivo)s" data-fancybox-group="gallery" title="%(iAssunto)s"><i class="icon-camera icon-white"></i> Visualizar</a>'% ({'iArquivo': str(iListaDocumentos[i].caminhoVisualizar), 'iAssunto': str(iListaDocumentos[i].assunto)})
                    #else:
                    iLinha= iLinha + '<a class="btn btn-primary" href="/download/%(iIDVersao)s/"><i class="icon-download-alt icon-white"></i>  Download</a>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                    
                    iLinha= iLinha + '<button class="btn btn-primary dropdown-toggle" data-toggle="dropdown"><span class="caret"></span></button><ul class="dropdown-menu">'
                    
                    if iListaDocumentos[i].visualizavel :
                        iLinha= iLinha + '<a class="fancybox" href="%(iArquivo)s" data-fancybox-group="gallery" title="%(iAssunto)s"><i class="icon-camera"></i> Visualizar</a>'% ({'iArquivo': str(iListaDocumentos[i].caminhoVisualizar), 'iAssunto': str(iListaDocumentos[i].assunto)})
                        #iLinha= iLinha + '<li><a href="/download/%(iIDVersao)s/"><i class="icon-download-alt"></i>  Download</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                    
                    iEstado = iListaDocumentos[i].id_estado
                    
                    if iEstado == constantes.cntEstadoVersaoPendente : #Aprovar/Reprovar
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/aprovar_documento/%(iIDVersao)s/"><i class="icon-thumbs-up"></i>  Aprovar</a></li><li><a class="fancybox fancybox.iframe" href="/reprovar_documento/%(iIDVersao)s/"><i class="icon-thumbs-down"></i>  Reprovar</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                    
                    if iEstado == constantes.cntEstadoVersaoDisponivel or iEstado == constantes.cntEstadoVersaoAprovado or iEstado == constantes.cntEstadoVersaoReprovado: #CheckOut
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/checkout/%(iIDVersao)s/"><i class="icon-edit"></i>  Check-out</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})
                        
                    if iEstado == constantes.cntEstadoVersaoDisponivel : #Encaminhar
                        iLinha= iLinha + '<li><a class="fancybox fancybox.iframe" href="/encaminhar/%(iIDVersao)s/"><i class="icon-share-alt"></i>  Encaminhar</a></li>'% ({'iIDVersao': str(iListaDocumentos[i].id_versao)})   
                        
                    if iEstado == constantes.cntEstadoVersaoBloqueado  : #CheckIn
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
def checkin(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        
        vIDFuncao = 0
        if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iPossuiPermissao= True
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get checkin: ' + str(e))
        return False
    
    if vRequest.POST:
        form = FormCheckin(vRequest.POST)
        if form.is_valid():
            try:
                Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoDisponivel)
                Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoCheckin, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
                return True
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel post checkin: ' + str(e))
                return False
        else:
            form = FormCheckin(vRequest.POST)
            iErro= True
    else: 
        form = FormCheckin()
                                           
    return render_to_response(
        'documentos/checkin.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def checkout(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        
        vIDFuncao = 0
        if not DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iPermissaoNegada= True
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get checkout: ' + str(e))
        return False
        
    if vRequest.POST:
        try :
            Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoBloqueado)
            Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoCheckout, 
                                   iUsuario.id, vRequest.session['IDEmpresa'])
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
        
        vIDFuncao = 0
        if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iPossuiPermissao= True
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get aprovar: ' + str(e))
        return False
    
    if vRequest.POST:
        try :
            if vRequest.POST.get('comentario') != '':
                Pendencia().adicionarFeedback(vIDVersao, vRequest.POST.get('comentario'))
                Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoAprovado)
                Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoAprovar, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
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
        
        vIDFuncao = 0
        if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iPossuiPermissao= True
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get reprovar: ' + str(e))
        return False
    
    if vRequest.POST:
        try :
            if vRequest.POST.get('comentario') != '':
                Pendencia().adicionarFeedback(vIDVersao, vRequest.POST.get('comentario'))
            Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoReprovado)
            Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoReprovar, 
                                   iUsuario.id, vRequest.session['IDEmpresa'])
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
        
        vIDFuncao = 0
        if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iPermissaoNegada= True
            
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get excluir: ' + str(e))
        return False
    
    if vRequest.POST:
        try :
            vIDFuncao = 0
            if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
                Versao().alterarEstadoVersao(vIDVersao, constantes.cntEstadoVersaoExcluida)
                Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoExcluir, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
            else:
                iPermissaoNegada= True
        except Exception, e:
                oControle.getLogger().error('Nao foi possivel post excluir: ' + str(e))
                return False
    return render_to_response(
        'acao/excluir.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def download(vRequest, vTitulo, vIDVersao=None):
    try :
        iUsuario= Usuario().obtemUsuario(vRequest.user)
        vIDFuncao  = 0
        if DocumentoControle().obtemPermissao(iUsuario.id, vIDFuncao):
            iArquivo= str(Versao().obtemCaminhoArquivo(vIDVersao))
            iFile = open(iArquivo,"r")
            response = HttpResponse(iFile.read())
            response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iArquivo)[1]
            Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoDownload, 
                                       iUsuario.id, vRequest.session['IDEmpresa'])
            return response
        else: 
            iPossuiPermissao= False
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
        iDiretorio=urllib.unquote(vRequest.POST.get('dir',''))
        vRequest.session['IDPasta'] = DocumentoControle().obtemIDPastaArvore(iDiretorio)
        iListaDocumentos = Versao().obtemListaDeDocumentosDaPasta(vRequest.session['IDEmpresa'], vRequest.session['IDPasta'])
        try:
            iHtml=['<ul class="jqueryFileTree" style="display: none;">']
            for iPasta in os.listdir(iDiretorio):
                iDiretorioFilho=os.path.join(iDiretorio, iPasta)
                if os.path.isdir(iDiretorioFilho):
                    iPasta= Pasta().obtemNomeDaPasta(iPasta)
                    iHtml.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (iDiretorioFilho, iPasta))
            iHtml.append('</ul>')
        except Exception,e:
            iHtml.append('Nao foi possivel carregar o diretorio: %s' % str(e))
        iHtml.append('</ul>')
        return HttpResponse(''.join(iHtml))
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel criar arvore: ' + str(e))
            return False
