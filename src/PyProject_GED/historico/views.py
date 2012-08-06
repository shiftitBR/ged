from django.shortcuts               import render_to_response
from django.template                import RequestContext

from models                         import Historico
from PyProject_GED.documento.models import Versao
from PyProject_GED.documento.models import Documento

def historico(vRequest, vTitulo, vIDVersao=None):
    
    iDocumento      = Documento().obtemInformacoesDocumento(vIDVersao)
    iListaVersao    = Versao().obtemListaDeVersoesDoDocumento(vIDVersao)
    iListaEventos   = Historico().obtemListaEventos(vIDVersao)
    
    iUltimaVersao   = iListaVersao[len(iListaVersao)-1].num_versao
    return render_to_response(
        'historico/historico.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )