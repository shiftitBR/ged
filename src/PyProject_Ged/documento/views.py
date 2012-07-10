from django.shortcuts       import render_to_response
from django.template        import RequestContext


def documentos(vRequest, vTitulo):
        
    return render_to_response(
        'documentos/documentos.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )