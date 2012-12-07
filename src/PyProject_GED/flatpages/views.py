# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.http                        import HttpResponse
from django.conf                        import settings

from PyProject_GED.autenticacao.models  import Empresa
from PyProject_GED.envioemail.models    import Publicacao_Documento, Publicacao, Publicacao_Usuario
from PyProject_GED.documento.models     import Versao
from PyProject_GED.documento.controle   import Controle as DocumentoControle

from objetos_auxiliares                 import Publicacao as PublicacaoAuxiliar
from PyProject_GED                      import oControle
from PyProject_GED                      import constantes
from django.contrib.auth.decorators     import login_required

import os

def home(vRequest, vTitulo):
    
    vRequest.session['id_pasta'] = ''
    
    return render_to_response(
        'home/home.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )

def enderecos(vRequest, vTitulo):
    
    iListaEnderecos= Empresa().obtemListaEnderecoEmpresas()
    
    return HttpResponse(iListaEnderecos)


def publicacao(vRequest, vTitulo, vIDPublicacao=None):
    
    iPublicacao                 = Publicacao().obtemPublicacao(vIDPublicacao)
    iListaPublicacaoDocumentos  = Publicacao_Documento().obtemListaPublicacaoDocumento(vIDPublicacao) 
    iListaPublicacaoUsuarios    = Publicacao_Usuario().obtemListaPublicacaoUsuario(vIDPublicacao)
    iListaPublicacao            = []
    iNomeRemetente              = iPublicacao.usr_remetente.first_name + ' ' + iPublicacao.usr_remetente.last_name
    
    for i in range(len(iListaPublicacaoDocumentos)):
        iVersao = Versao().obtemVersaoAtualDoDocumento(iListaPublicacaoDocumentos[i].documento)
        iPublicacaoAux                      = PublicacaoAuxiliar()
        iPublicacaoAux.nome_arquivo         = iVersao.upload.filename.encode('utf-8')
        iPublicacaoAux.assunto              = iListaPublicacaoDocumentos[i].documento.assunto
        iPublicacaoAux.nome_remetente       = iNomeRemetente
        iPublicacaoAux.tipo_visuzalizacao   = DocumentoControle().tipoVisualizavel(iVersao.upload.filename.encode('utf-8'))
        iPublicacaoAux.caminho_visualizar   = DocumentoControle().obtemCaminhoVisualizar(str(iVersao.upload.image))
        iPublicacaoAux.id_versao            = iVersao.id_versao
        iListaPublicacao.append(iPublicacaoAux)
        
    return render_to_response(
        'publicacao/publicacao.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def sucesso(vRequest, vTitulo, vAcao=None):
    iAcao = int(vAcao)
    if iAcao == constantes.cntFuncaoCheckinChekout:
        iMensagem = 'A ação sobre o documento foi efetuada com sucesso.'
    elif iAcao == constantes.cntFuncaoAprovarReprovar:
        iMensagem = 'A ação sobre o documento foi efetuada com sucesso.'
    elif iAcao == constantes.cntFuncaoEncaminhar:
        iMensagem = 'O documento foi encaminhado com sucesso.'
    elif iAcao == constantes.cntFuncaoExcluir:
        iMensagem = 'O documento foi excluido com sucesso.'
    elif iAcao == constantes.cntFuncaoDigitalizar:
        iMensagem = 'O documento foi digitalizado com sucesso'
    elif iAcao == constantes.cntFuncaoImportar:
        iMensagem = 'A importação foi feita com sucesso.'
    elif iAcao == constantes.cntFuncaoAssinar:
        iMensagem = 'A assinatura foi feita com sucesso.'    
    elif iAcao == constantes.cntFuncaoEmail:
        iMensagem = 'O e-mail foi enviado com sucesso.'  
    elif iAcao == constantes.cntFuncaoPublicar:
        iMensagem = 'A publicação foi encaminhada com sucesso.'      
    elif iAcao == constantes.cntFuncaoDigitalizar:
        iMensagem = 'A Imagem foi Digitalizada com sucesso.' 
    
    return render_to_response(
        'mensagem/sucesso.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
    
def ajuda(vRequest, vTitulo):
    
    return render_to_response(
        'ajuda/ajuda.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )

@login_required 
def download_importador(vRequest, vTitulo):
    try :
        iCaminhoArquivo = settings.PROJECT_ROOT_PATH + "/" + settings.MEDIA_URL + "ajuda/Importador.rar"
        iFile = open(iCaminhoArquivo,"r")
        iResponseP7s = HttpResponse(iFile.read())
        iResponseP7s["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iCaminhoArquivo)[1]
        return iResponseP7s        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel fazer download do arquivo Importador: ' + str(e))
            return False
        
@login_required 
def download_biometria(vRequest, vTitulo):
    try :
        iCaminhoArquivo = settings.PROJECT_ROOT_PATH + "/" + settings.MEDIA_URL + "ajuda/Biometria.rar"
        iFile = open(iCaminhoArquivo,"r")
        iResponseP7s = HttpResponse(iFile.read())
        iResponseP7s["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iCaminhoArquivo)[1]
        return iResponseP7s        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel fazer download do arquivo Biometria: ' + str(e))
            return False