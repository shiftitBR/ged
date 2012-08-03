from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from PyProject_GED.documento.models     import Versao
from PyProject_GED.indice.forms         import FormBuscaDocumento

    
def busca(vRequest, vTitulo):
    if vRequest.method == 'POST':
        form = FormBuscaDocumento(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        iAssunto= vRequest.POST.get('assunto')
        iProtocolo= vRequest.POST.get('protocolo')
        #iUsuarioResponsavel= vRequest.POST.get('usuario_responsavel')
        iListaDocumentos= Versao().buscaDocumentos(iAssunto, iProtocolo)
    else:
        form = FormBuscaDocumento(iIDEmpresa=vRequest.session['IDEmpresa'])        
        
    return render_to_response(
        'busca/busca.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )