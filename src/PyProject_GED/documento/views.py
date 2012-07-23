# -*- coding: utf-8 -*-
from django.shortcuts               import render_to_response
from django.template                import RequestContext
from django.http                    import HttpResponse

from PyProject_GED                  import oControle
from controle                       import Controle as DocumentoControle

from django.contrib.auth.decorators import login_required

import os
import urllib

@login_required 
def documentos(vRequest, vTitulo):
    try :
        iPasta_Raiz = oControle.getPasta()
        iListaDocumentos=[]
        if oControle.getIDPasta() != '':
            iListaDocumentos = DocumentoControle().obtemListaDocumentos(oControle.getIDPasta())
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get documentos: ' + str(e))
            return False
        
    if vRequest.POST:
        try :
            iListaCheck=[]
            iListaVersao = ''
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
        iPasta_Raiz = oControle.getPasta()
        iListaDocumentos=[]
        if oControle.getIDPasta() != '':
            iListaDocumentos = DocumentoControle().obtemListaDocumentos(oControle.getIDPasta())
            iHtml= []
            for i in range(len(iListaDocumentos)):     
                iLinha= '<tr><td><label class="checkbox"><input type="checkbox" value="option1" name="versao_%(iIDVersao)s"></label></td><td><center>%(iProtocolo)s</center></td><td>%(iAssunto)s</td><td>%(iTipo)s</td><td>%(iEstado)s</td><td>%(iUsuario)s</td><td><center>%(iVersao)s</center></td><td><center>%(iData)s</center></td><td><div class="btn-group"><a class="btn btn-primary" href="/download/%(iIDVersao)s/"><i class="icon-download-alt icon-white"></i>  Download</a><button data-toggle="dropdown" class="btn btn-primary dropdown-toggle"><span class="caret"></span></button><ul class="dropdown-menu"><li><a href="/aprovar_documento/%(iIDVersao)s/" class="fancybox fancybox.iframe"><i class="icon-thumbs-up"></i>  Aprovar</a></li><li><a href="/reprovar_documento/%(iIDVersao)s/" class="fancybox fancybox.iframe"><i class="icon-thumbs-down"></i>  Reprovar</a></li><li><a href="/checkout/%(iIDVersao)s/" class="fancybox fancybox.iframe"><i class="icon-edit"></i>  Check-out</a></li><li><a href="/checkin/%(iIDVersao)s/" class="fancybox fancybox.iframe"><i class="icon-share"></i>  Check-in</a></li><li class="divider"></li><li><a href="/excluir_documento/%(iIDVersao)s/" class="fancybox fancybox.iframe"><i class="icon-trash"></i>  Excluir</a></li><li class="divider"></li><li><a href="/historico/%(iIDVersao)s/" class="fancybox fancybox.iframe"><i class="icon-book"></i>  Histórico</a></li><li><a href="/informacoes_documento/%(iIDVersao)s/" class="fancybox fancybox.iframe"><i class="icon-info-sign"></i>  Informações</a></li></ul></div></td></tr>' % (
                          {'iVersao': str(iListaDocumentos[i].num_versao), 
                           'iIDVersao': str(iListaDocumentos[i].id_versao),
                           'iProtocolo': str(iListaDocumentos[i].protocolo), 
                           'iAssunto': str(iListaDocumentos[i].assunto),
                           'iTipo': str(iListaDocumentos[i].tipo_documento), 
                           'iEstado': str(iListaDocumentos[i].estado), 
                           'iUsuario': str(iListaDocumentos[i].criador), 
                           'iData': str(iListaDocumentos[i].data_criacao)
                           })
                iHtml.append(iLinha)
            return HttpResponse(''.join(iHtml))
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tabela documentos: ' + str(e))
            return False

@login_required     
def checkin(vRequest, vTitulo, vIDVersao=None):
    try :
        print ''
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tela checkin: ' + str(e))
            return False
    return render_to_response(
        'documentos/checkin.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def checkout(vRequest, vTitulo, vIDVersao=None):
    try :
        print ''
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tela checkout: ' + str(e))
            return False
    return render_to_response(
        'documentos/checkout.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def aprovar(vRequest, vTitulo, vIDVersao=None):
    try :
        print ''
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tela aprovar: ' + str(e))
            return False
    return render_to_response(
        'acao/aprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def reprovar(vRequest, vTitulo, vIDVersao=None):
    try :
        print ''
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tela reprovar: ' + str(e))
            return False
    return render_to_response(
        'acao/reprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def excluir(vRequest, vTitulo, vIDVersao=None):
    try :
        print ''
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tela excluir: ' + str(e))
            return False
    return render_to_response(
        'acao/excluir.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def informacoes(vRequest, vTitulo, vIDVersao=None):
    try :
        print ''
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel abrir tela informacoes: ' + str(e))
            return False
    return render_to_response(
        'documentos/informacoes.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def download(vRequest, vTitulo, vIDVersao=None):
    try :
        iArquivo= str(DocumentoControle().obtemCaminhoArquivo(vIDVersao))
        iFile = open(iArquivo,"r")
        response = HttpResponse(iFile.read())
        response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iArquivo)[1]
        return response
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel fazer download do arquivo: ' + str(e))
            return False
    
@login_required 
def criaArvore(vRequest, vTitulo):
    try :
        iDiretorio=urllib.unquote(vRequest.POST.get('dir',''))
        if iDiretorio[len(iDiretorio)-1] != '/': #sem / no final
            oControle.setIDPasta(os.path.basename(iDiretorio))
        else :
            iIDPasta= iDiretorio.replace(' ', '')[:-1] #com / no final = retirar / do final
            oControle.setIDPasta(os.path.basename(iIDPasta)) 
            iListaDocumentos = DocumentoControle().obtemListaDocumentos(oControle.getIDPasta())
        try:
            iHtml=['<ul class="jqueryFileTree" style="display: none;">']
            for iPasta in os.listdir(iDiretorio):
                iDiretorioFilho=os.path.join(iDiretorio, iPasta)
                if os.path.isdir(iDiretorioFilho):
                    iPasta= DocumentoControle().obtemNomeDaPasta(iPasta)
                    iHtml.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (iDiretorioFilho, iPasta))
            iHtml.append('</ul>')
            #iHtml.append('<div class="teste">{{iListaDocumentos}}</div>')
        except Exception,e:
            iHtml.append('Could not load directory: %s' % str(e))
        iHtml.append('</ul>')
        return HttpResponse(''.join(iHtml))
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel criar arvore: ' + str(e))
            return False
