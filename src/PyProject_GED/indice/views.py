# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger
from PyProject_GED.documento.models     import Versao
from PyProject_GED.indice.forms         import FormBuscaDocumento
from PyProject_GED.indice.models        import Indice, Indice_Pasta
from PyProject_GED                      import oControle, constantes
import datetime

    
def busca(vRequest, vIDTipoBusca, vTitulo):
    iIDEmpresa= vRequest.session['IDEmpresa']
    if int(vIDTipoBusca) == constantes.cntTipoBuscaPorPasta:
        iIDPastaSelecionada= vRequest.session['IDPasta']
        iListaIndices= Indice_Pasta().obtemIndicesDaPasta(iIDPastaSelecionada)
    else:
        iIDPastaSelecionada= None
        iListaIndices= Indice().obtemListaIndices(iIDEmpresa)
    
    print '>>>>>>>>>>>>>>>>>>..'
    for iIndiceX in iListaIndices:
        print iIndiceX.descricao
        
    try:
        iListaDoc = vRequest.session['ListaBusta']
    except:
        iListaDoc = []
    
    try:
        iPaginator  = Paginator(iListaDoc, 10)
        iPage       = vRequest.GET.get('page')
        if iPage == None:
            iPage = 1
        try:
            iDocumentos = iPaginator.page(iPage)
        except PageNotAnInteger:
            iDocumentos = iPaginator.page(1)
        except EmptyPage:
            iDocumentos = iPaginator.page(iPaginator.num_pages)
    except:
        iDocumentos=[]
    
    if vRequest.method == 'POST':
        form = FormBuscaDocumento(vRequest.POST, iIDEmpresa= iIDEmpresa)
        try:
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
            iIDUsuario= vRequest.user.id
            
            if iDataInicio not in (None, ''):
                iDataInicio= datetime.datetime.strptime(iDataInicio + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
                
            if iDataFim not in (None, ''):
                iDataFim= datetime.datetime.strptime(iDataFim + ' 23:59:59', '%d/%m/%Y %H:%M:%S')
            
            if 'buscaAcancada' in vRequest.POST:
                for i in range(len(iListaIndices)):
                    iIndice= vRequest.POST.get('indice_%s' % iListaIndices[i].id_indice)
                    if iIndice not in (None, ''):
                        iListaIDIndices.append((iListaIndices[i].id_indice, iIndice))  
            iListaDocumentos= Versao().buscaDocumentos(iIDEmpresa, iAssunto, iProtocolo, iUsuarioResponsavel, 
                                                       iUsuarioCriador, iTipoDocumento, iEstado, iDataInicio, 
                                                       iDataFim, iListaIDIndices, iConteudo, iNormas, 
                                                       iIDUsuario, iIDPastaSelecionada, vEhPublico= False)
            iPaginator = Paginator(iListaDocumentos, 10)
            iDocumentos = iPaginator.page(1)
            vRequest.session['ListaBusta']= iListaDocumentos
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post documentos: ' + str(e))
            return False
    else:
        form = FormBuscaDocumento(iIDEmpresa= iIDEmpresa)        
        
    return render_to_response(
        'busca/busca.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def publico(vRequest, vTitulo, vIDEmpresa):
    iListaIndices= Indice().obtemListaIndices(vIDEmpresa)
    if vRequest.method == 'POST':
        form = FormBuscaDocumento(vRequest.POST, iIDEmpresa= vIDEmpresa)
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
            for i in range(len(iListaIndices)):
                iIndice= vRequest.POST.get('indice_%s' % iListaIndices[i].id_indice)
                if iIndice not in (None, ''):
                    iListaIDIndices.append((iListaIndices[i].id_indice, iIndice))  
        iListaDocumentos= Versao().buscaDocumentos(vIDEmpresa, iAssunto, iProtocolo, iUsuarioResponsavel, 
                                                   iUsuarioCriador, iTipoDocumento, iEstado, iDataInicio, 
                                                   iDataFim, iListaIDIndices, iConteudo, vEhPublico= True)
    else:
        form = FormBuscaDocumento(iIDEmpresa= vIDEmpresa)        
        
    return render_to_response(
        'publico/publico.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )