from django.shortcuts       import render_to_response
from django.template        import RequestContext

    
def busca(vRequest, vTitulo):
    
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
    
    for i in range(15):    
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
    
    return render_to_response(
        'busca/busca.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )