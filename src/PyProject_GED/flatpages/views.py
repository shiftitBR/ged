from django.shortcuts       import render_to_response
from django.template        import RequestContext


def home(vRequest, vTitulo):

    return render_to_response(
        'home/home.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )

    

    
