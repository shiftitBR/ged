from django.shortcuts       import render_to_response
from django.template        import RequestContext


def historico(vRequest, vTitulo, vIDVersao=None):
    
    return render_to_response(
        'historico/historico.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )