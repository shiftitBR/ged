from django.shortcuts       import render_to_response
from django.template        import RequestContext

    
def busca(vRequest, vTitulo):
    
    return render_to_response(
        'busca/busca.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )