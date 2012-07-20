from django.shortcuts               import render_to_response, get_object_or_404
from django.template                import RequestContext
from django.http                    import HttpResponse

from PyProject_GED                  import oControle
from controle                       import Controle as DocumentoControle
from indice.controle                import Controle as IndiceControle   #@UnresolvedImport

from forms                          import FormUploadDeArquivo

from django.contrib.auth.decorators import login_required

import os
import urllib
from mimetypes import MimeTypes
from django.conf import settings

@login_required 
def documentos(vRequest, vTitulo):
    
    iPasta_Raiz = oControle.getPasta()
    iListaDocumentos=[]
    if oControle.getIDPasta() != '':
        iListaDocumentos = DocumentoControle().obtemListaDocumentos(oControle.getIDPasta())
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
    
@login_required 
def checkin(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'documentos/checkin.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def checkout(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'documentos/checkout.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def importar(vRequest, vTitulo):
    iUser = vRequest.user
    if iUser:
        iUsuario= DocumentoControle().obtemUsuario(iUser)
    
    iListaTipoDocumento = DocumentoControle().obtemListaTipoDocumento()
    iListaIndices       = DocumentoControle().obtemListaIndices()
    #gerarProtocolo

    if vRequest.method == 'POST':
        print '>>>>>>>>>>>>>>>>>> entrou_importar'
        form = FormUploadDeArquivo(vRequest.POST)
        if form.is_valid(): 
            iAssunto    = vRequest.POST.get('assunto')
            if vRequest.POST.get('eh_publico') != None:
                iEh_Publico = True
            else:
                iEh_Publico = False
            iIDTipo_Documento = vRequest.POST.get('tipo_documento')
            iDocumento  = DocumentoControle().salvaDocumento(iIDTipo_Documento, iUsuario, 
                                            oControle.getIDPasta(), iAssunto, iEh_Publico)
            iVersao     = DocumentoControle().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                            1, 1, 'Teste.jpg', '1234567')
            #Salvar Indices
            for i in range(len(iListaIndices)):
                iIndice = iListaIndices[i]
                iValor  = vRequest.POST.get('indice_%s' % iIndice.id_indice)
                if iValor != '':
                    IndiceControle().salvaValorIndice(iValor, iIndice.id_indice, iVersao.id_versao)
    else:
        form = FormUploadDeArquivo()
        
    return render_to_response(
        'documentos/importar_doc.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def aprovar(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'acao/aprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def reprovar(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'acao/reprovar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def excluir(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'acao/excluir.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def informacoes(vRequest, vTitulo, vIDVersao=None):
        
    return render_to_response(
        'documentos/informacoes.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def download(vRequest, vTitulo, vIDVersao=None):
    #iArquivo= DocumentoControle().obtemCaminhoArquivo(vIDVersao)
    iArquivo= "%s/multiuploader_images/"%(settings.MEDIA_ROOT,) + oControle.getBanco() +"/%s" % ('midi.odt', )
    iFile = open(iArquivo,"r")
    response = HttpResponse(iFile.read())
    response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iArquivo)[1]
    return response
    
@login_required 
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
