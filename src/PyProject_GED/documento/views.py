from django.shortcuts       import render_to_response
from django.template        import RequestContext

import os
import urllib
from django.http import HttpResponse


def documentos(vRequest, vTitulo):
    print '>>>>>>>>>>>>   documentos'
    
    print vRequest.session['id_pasta']
    
    class Documento():
        id= None
        id_versao=None
        assunto= None
        pasta= None
        tipo_documento= None
        versao_atual= None
        publico= None
        responsavel= None
        descarte= None
        validade= None
        data_criacao=None
        versao=None
        descricao=None
        criador=None
        arquivo=None
        estado=None
        id_estado=None
        protocolo=None
        assinado=None
    
    iListaDocumentos=[]
    
    for i in range(10):    
        iDocumento= Documento()
        iDocumento.id= 1
        iDocumento.versao_atual= 5
        iDocumento.publico= True
        iDocumento.id_versao= i
        iDocumento.assunto= 'teste_' + str(i)
        iDocumento.pasta= '/documentos/'
        iDocumento.tipo_documento= 'Modelo'
        iDocumento.responsavel= 'Diego C.'
        iDocumento.descarte= '01/01/2012'
        iDocumento.validade= '21/12/2012'
        iDocumento.data_criacao= '01/01/2012'
        iDocumento.versao= i
        iDocumento.descricao='Teste Documento'
        iDocumento.criador='Alexandre S.'
        iDocumento.arquivo='teste.odt'
        iDocumento.estado='Disponivel'
        iDocumento.id_estado=1
        iDocumento.protocolo=1234567
        iDocumento.assinado=False
        iListaDocumentos.append(iDocumento)
    
    iPasta = '/home/diego/ged_documentos/'
            
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
        vRequest.session['id_pasta'] = os.path.basename(iDiretorio)
    else :
        iIDPasta= iDiretorio.replace(' ', '')[:-1] #com / no final = retirar / do final
        vRequest.session['id_pasta'] = os.path.basename(iIDPasta)
    try:
        iHtml=['<ul class="jqueryFileTree" style="display: none;">']
        for iPasta in os.listdir(iDiretorio):
            iDiretorioFilho=os.path.join(iDiretorio,iPasta)
            #iPasta= nomePasta(iPasta)
            if os.path.isdir(iDiretorioFilho):
                iHtml.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (iDiretorioFilho, iPasta))
        iHtml.append('</ul>')
    except Exception,e:
        iHtml.append('Could not load directory: %s' % str(e))
    iHtml.append('</ul>')
    return HttpResponse(''.join(iHtml))
    