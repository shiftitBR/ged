'''
Created on Jul 11, 2012

@author: Shift IT | www.shiftit.com.br
'''
from django.conf    import settings


#Configuracoes
cntConfiguracaoDiretorioDocumentos= settings.MEDIA_ROOT + '/documentos/empresa_%03d'
cntConfiguracaoPastaDocumentos= 'documentos'

#Eventos
cntEventoHistoricoCheckIn   = 1
cntEventoHistoricoCheckout  = 2
cntEventoHistoricoAprovar   = 3
cntEventoHistoricoReprovar  = 4
cntEventoHistoricoExcluir   = 5
cntEventoHistoricoDownload  = 6
cntEventoHistoricoVisualizar= 7
cntEventoHistoricoEncaminhar= 8

#Estados da Versao
cntEstadoVersaoDisponivel   = 1
cntEstadoVersaoBloqueado    = 2
cntEstadoVersaoAprovado     = 3
cntEstadoVersaoReprovado    = 4
cntEstadoVersaoExcluida     = 5
cntEstadoVersaoObsoleto     = 6
cntEstadoVersaoPendente     = 7

