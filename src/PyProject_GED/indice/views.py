from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from PyProject_GED.documento.models     import Versao
from PyProject_GED.indice.forms         import FormBuscaDocumento
from PyProject_GED.indice.models import Indice

    
def busca(vRequest, vTitulo):
    iIDEmpresa= vRequest.session['IDEmpresa']
    iListaIndices= Indice().obtemListaIndices(iIDEmpresa)
    if vRequest.method == 'POST':
        form = FormBuscaDocumento(vRequest.POST, iIDEmpresa= iIDEmpresa)
        iAssunto= vRequest.POST.get('assunto')
        iProtocolo= vRequest.POST.get('protocolo')
        iConteudo= vRequest.POST.get('conteudo')
        iDataInicio= vRequest.POST.get('data_criacao_inicial')
        iDataFim= vRequest.POST.get('data_criacao_final')
        iUsuarioResponsavel= vRequest.POST.get('usuario_responsavel')
        iUsuarioCriador= vRequest.POST.get('usuario_criador')
        iNormas= vRequest.POST.get('normas')
        iTipoDocumento= vRequest.POST.get('tipo_documento')
        iEstado= vRequest.POST.get('estado')
        iConteudo= vRequest.POST.get('conteudo')
        iListaIDIndices= []
        if 'buscaAcancada' in vRequest.POST:
            print vRequest.POST
            for i in range(len(iListaIndices)):
                iIndice= vRequest.POST.get('indice_%s' % iListaIndices[i].id_indice)
                if iIndice not in (None, ''):
                    iListaIDIndices.append((iListaIndices[i].id_indice, iIndice))  
        iListaDocumentos= Versao().buscaDocumentos(iIDEmpresa, iAssunto, iProtocolo, iUsuarioResponsavel, 
                                                   iUsuarioCriador, iTipoDocumento, iEstado, iDataInicio, 
                                                   iDataFim, iListaIDIndices, iConteudo)
    else:
        form = FormBuscaDocumento(iIDEmpresa= iIDEmpresa)        
        
    return render_to_response(
        'busca/busca.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )