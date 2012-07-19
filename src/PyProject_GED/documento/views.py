from django.shortcuts               import render_to_response
from django.template                import RequestContext
from django.http                    import HttpResponse

from PyProject_GED                  import oControle
from controle                       import Controle as DocumentoControle

from forms                          import FormUploadDeArquivo

import os
import urllib

def documentos(vRequest, vTitulo):
    
    iPasta_Raiz = oControle.getPasta()
    iListaDocumentos=[]
    if oControle.getIDPasta() != '':
        iListaDocumentos = DocumentoControle().obtemListaDocumentos(oControle.getIDPasta())
        print '>>>>>>>>>>>>>> ListaDocumentos - Documentos'
        print iListaDocumentos
    iTeste = len(iListaDocumentos)
    
    if vRequest.POST:
        
        iListaCheck=[]
        iListaVersao = ''
        for i in range(len(iListaDocumentos)): 
            if 'versao_%s' % iListaDocumentos[i].id_versao in vRequest.POST:
                iListaCheck.append(iListaDocumentos[i].id_versao)
                iListaVersao = str(iListaDocumentos[i].id_versao) + iListaVersao
    
    return render_to_response(
        'documentos/documentos.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def checkin(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'documentos/checkin.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def checkout(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'documentos/checkout.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def importar(vRequest, vTitulo):
    iUser = vRequest.user
    if iUser:
        iUsuario= DocumentoControle().obtemUsuario(iUser)
    
    iListaTipoDocumento = DocumentoControle().obtemListaTipoDocumento()
    iListaIndices       = DocumentoControle().obtemListaIndices()
    #gerarProtocolo

    if vRequest.method == 'POST':
        print '>>>>>>>>>>.. entrouuuuu'
        form = FormUploadDeArquivo(vRequest.POST)
        if form.is_valid(): 
            iAssunto= vRequest.POST.get('assunto')
            if vRequest.POST.get('eh_publico') != None:
                iEh_Publico = True
            else: 
                iEh_Publico = False
            iIDTipo_Documento = DocumentoControle().obtemIDTipoDocumento(vRequest.POST.get('tipo_documento'))
                    
            print vRequest.POST.get('arquivo')
            print vRequest.POST.get('datavalidade')
            print vRequest.POST.get('inputDate')
    else:
        form = FormUploadDeArquivo()
        
    return render_to_response(
        'documentos/importar_doc.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def aprovar(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'acao/aprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def reprovar(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'acao/reprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def excluir(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'acao/excluir.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
def informacoes(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'documentos/informacoes.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )

def criaArvore(vRequest, vTitulo):
    iDiretorio=urllib.unquote(vRequest.POST.get('dir',''))
    if iDiretorio[len(iDiretorio)-1] != '/': #sem / no final
        oControle.setIDPasta(os.path.basename(iDiretorio))
    else :
        iIDPasta= iDiretorio.replace(' ', '')[:-1] #com / no final = retirar / do final
        oControle.setIDPasta(os.path.basename(iIDPasta))
    try:
        iHtml=['<ul class="jqueryFileTree" style="display: none;">']
        for iPasta in os.listdir(iDiretorio):
            iDiretorioFilho=os.path.join(iDiretorio, iPasta)
            iPasta= DocumentoControle().obtemNomeDaPasta(iPasta)
            if os.path.isdir(iDiretorioFilho):
                iHtml.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (iDiretorioFilho, iPasta))
        iHtml.append('</ul>')
    except Exception,e:
        iHtml.append('Could not load directory: %s' % str(e))
    iHtml.append('</ul>')
    return HttpResponse(''.join(iHtml))
    