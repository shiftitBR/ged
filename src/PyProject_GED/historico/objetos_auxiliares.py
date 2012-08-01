
class Documento():
    idDocumento=None
    assunto=None
    dscTipoDoc=None
    versaoAtual=None
    nomeResponsavel=None
    nomePasta=None
    dataValidade=None
    dataDescarte=None
    ehPublico=None
    totalDownloads=None
    totalVisualizacao=None
    
class Versoes():
    idVersao=None
    num_versao=None
    dsc_modificacao=None
    nomeCriador=None
    nomeArquivo=None
    estado=None
    idEstado=None
    protocolo=None
    ehAssinado=None
    

class Historico():
    idHistorico=None
    dataEvento=None
    idTipoEvento= None
    dscEvento=None
    num_versao=None
    dsc_modificacao=None
    nomeUsuario=None
