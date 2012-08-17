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
cntEventoHistoricoObsoletar = 9
cntEventoHistoricoEmail     = 10
cntEventoHistoricoPublicar  = 11

#Estados da Versao
cntEstadoVersaoDisponivel   = 1
cntEstadoVersaoBloqueado    = 2
cntEstadoVersaoAprovado     = 3
cntEstadoVersaoReprovado    = 4
cntEstadoVersaoExcluida     = 5
cntEstadoVersaoObsoleto     = 6
cntEstadoVersaoPendente     = 7

#TipoVisualizacao
cntTipoVisualizacaoPDF      = 1
cntTipoVisualizacaoImagem   = 2
cntTipoVisualizacaoOutro    = 3

#OCR
cntOCRExtencaoDocumentoTexto= 'ocr'
cntOCRExtencoesImagens      = ['.jpg', '.png', '.tif', '.bmp']
cntOCRExtencoesDocumentos   = ['.doc', '.docx', '.odt']
cntOCRExtencoesTextos       = ['.txt', '.ocr']
cntOCRExtencoesPDF          = ['.pdf',]

#TipoUsuario
cntTipoUsuarioSistema       = 1
cntTipoUsuarioContato       = 2

#Tipo Erro Login
cntTipoErroSenhaUser        = 1
cntTipoErroInativo          = 2
cntTipoErroIpBloqueado      = 3
cntTipoErroEmpresaInativa   = 4
