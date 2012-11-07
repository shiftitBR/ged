'''
Created on Jul 11, 2012

@author: Shift IT | www.shiftit.com.br
'''
from django.conf    import settings


#Configuracoes
cntConfiguracaoDiretorioDocumentos      = settings.MEDIA_ROOT + '/documentos/empresa_%03d'
cntConfiguracaoPastaDocumentos          = 'documentos'
cntConfiguracaoDiasAvisoVencimento      = 5
cntConfiguracaoEmailAlerta              = 'alerta@trackdoc.com.br'
cntConfiguracaoIDGrupoAdministradores   = '1'
cntConfiguracaoDominio                  = 'trackdoc.com.br'
cntConfiguracaoIPServidor               = '54.243.50.54'

#Servicos
cntServicosEnviaAlertaPendencia= 1

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
cntEventoHistoricoLogin     = 12
cntEventoHistoricoCancelarPendencia= 13
cntEventoHistoricoRelatorio = 14
cntEventoHistoricoImportar  = 15
cntEventoHistoricoExportar  = 16
cntEventoHistoricoAssinar   = 17
cntEventoHistoricoCadastraContato= 18
cntEventoHistoricoDigitalizar= 19

#Estados da Versao
cntEstadoVersaoDisponivel   = 1
cntEstadoVersaoBloqueado    = 2
cntEstadoVersaoAprovado     = 3
cntEstadoVersaoReprovado    = 4
cntEstadoVersaoExcluida     = 5
cntEstadoVersaoObsoleto     = 6
cntEstadoVersaoPendente     = 7
cntEstadoVersaoVencido      = 8

#Estados da Pendencia
cntEstadoPendenciaPendente  = 1
cntEstadoPendenciaConcluida = 2
cntEstadoPendenciaCancelada = 3

#Tipo da Pendencia
cntTipoPendenciaAprovacao   = 1
cntTipoPendenciaAssintaura  = 2

#Acao da Pendencia
cntAcaoPendenciaAprovar     = 1
cntAcaoPendenciaReprovar    = 2
cntAcaoPendenciaAssinar     = 3
cntAcaoPendenciaCancelar    = 4


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

#TipoRelatorio
cntTipoRelatorioAcessos     = 1
cntTipoRelatorioUsuario     = 2

#Funcoes
cntFuncaoDownload           = 1
cntFuncaoCheckinChekout     = 2
cntFuncaoAprovarReprovar    = 3
cntFuncaoEncaminhar         = 4
cntFuncaoExcluir            = 5
cntFuncaoHistorico          = 6
cntFuncaoVisualizar         = 7
cntFuncaoDigitalizar        = 8
cntFuncaoImportar           = 9
cntFuncaoAssinar            = 10
cntFuncaoAssociarNorma      = 11
cntFuncaoEmail              = 12
cntFuncaoPublicar           = 13
cntFuncaoRelatorio          = 14
cntFuncaoExportar           = 15
cntFuncaoCadastrarContato   = 16

#Redireciona Contato
cntRedirecionaEmail         = 1
cntRedirecionaPublicacao    = 2

#Extencoes de Imagem
cntExtencaoImagemExportavel = ['.jpg', '.png', '.tif', '.bmp']
cntExtencaoImagemJPG        = 1
cntExtencaoImagemPNG        = 2
cntExtencaoImagemBMP        = 3
cntExtencaoImagemTIF        = 4

#Extencoes Comprimiveis
cntExtencaoImagemComprimivel= ['.jpg', '.gif', '.png', '.jpeg']

#Extencoes Certificados
cntExtencaoCertificado      = ['.pfx']

#Tipos de Email
cntTipoEmailPendenciaRecebida   = 1
cntTipoEmailPendenciaAprovada   = 2
cntTipoEmailPendenciaReprovada  = 3
cntTipoEmailDocumentoVencendo   = 4

#Tipo de Busca
cntTipoBuscaGeral               = 1
cntTipoBuscaPorPasta            = 2

#Importacao FTP
cntImportacaoFTPPastaRaiz       = '/home/trackdoc'

#Servidor FTP
cntServidorFTPIP                = '54.243.50.54'
cntServidorFTPLogin             = 'trackdoc'
cntServidorFTPSenha             = 'trk@D0C+412'

#Socket TCP
cntSocketTCPIP                  = '0.0.0.0'
cntSocketTCPPorta               = 7043

#Tipo Mesagem JSON
cntTipoMensagemJSONNormal       = '1'
cntTipoMensagemJSONErro         = '2'

#Classe Mesagem JSON
cntClasseMensagemImportacao     = '1'
cntClasseMensagemLogin          = '2'
cntClasseMensagemCadastro       = '3'
cntClasseMensagemConfirmacao    = '4'

#Edicao Imagem
cntEdicaoImagemRotacaoDireita   = 1
cntEdicaoImagemRotacaoEsquerda  = 2
cntEdicaoImagemGraus            = 90
