from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.http                        import HttpResponse
from django.conf                        import settings

from PyProject_GED.autenticacao.models  import Empresa
from PyProject_GED.envioemail.models    import Publicacao_Documento, Publicacao, Publicacao_Usuario
from PyProject_GED.documento.models     import Versao
from PyProject_GED.documento.controle   import Controle as DocumentoControle

from objetos_auxiliares                 import Publicacao as PublicacaoAuxiliar

def home(vRequest, vTitulo):
    
    vRequest.session['id_pasta'] = ''
    vRequest.session.set_expiry(6000)
    
    settings.request = vRequest
    
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
        iListaPublicacao.append(iPublicacaoAux)
        
    return render_to_response(
        'publicacao/publicacao.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )