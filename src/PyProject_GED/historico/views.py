from django.shortcuts       import render_to_response
from django.template        import RequestContext

from models                 import Historico

def historico(vRequest, vTitulo, vIDVersao=None):
    
    iDocumento      = Historico().obtemInformacoesDocumento(vIDVersao)
    iListaVersao    = Historico().obtemListaVersao(vIDVersao)
    iListaEventos   = Historico().obtemListaEventos(vIDVersao)
    
    iUltimaVersao   = iListaVersao[len(iListaVersao)-1].num_versao
    return render_to_response(
        'historico/historico.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )