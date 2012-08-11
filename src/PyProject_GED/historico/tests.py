
from django.test                            import TestCase
from django.contrib.auth.models             import User

from models                                 import Tipo_de_Evento

import datetime
from PyProject_GED.autenticacao.models      import Empresa, Usuario,\
    Tipo_de_Usuario
from PyProject_GED.seguranca.models         import Pasta
from PyProject_GED.documento.models         import Tipo_de_Documento, Documento, Estado_da_Versao, Versao
from PyProject_GED.multiuploader.models     import MultiuploaderImage
from PyProject_GED.historico.models         import Historico

import constantes #@UnresolvedImport

class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarTipoUsuario()
        self.mokarUsuario()
        self.mokarPasta()
        self.mokarTipoDocumento()
        self.mokarMultiUploader()
        self.mokarDocumento()
        self.mokarEstadoVersao()
        self.mokarCriarVersao()
        self.mokarTipoDeEvento()
        self.mokarEventos()
        pass

    def tearDown(self):
        Tipo_de_Evento.objects.all().delete()
        Versao.objects.all().delete()
        Estado_da_Versao.objects.all().delete()
        Documento.objects.all().delete()
        MultiuploaderImage.objects.all().delete()
        Tipo_de_Documento.objects.all().delete()
        Pasta.objects.all().delete()
        Usuario.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Empresa.objects.all().delete()
        Historico.objects.all().delete()
        Tipo_de_Evento.objects.all().delete()
        pass


    def testCriarTipoDeEvento(self):
        iDescricao= 'Evento teste'
        iTipoDeEvento= Tipo_de_Evento()
        iTipoDeEvento.descricao= iDescricao
        iTipoDeEvento.save()
        self.assertEquals(1, len(Tipo_de_Evento.objects.filter(descricao= iDescricao)))
        
    def testCriarHistorico(self):
        iHistorico= Historico()
        iHistorico.versao= Versao.objects.all()[0]
        iHistorico.tipo_evento= Tipo_de_Evento.objects.all()[0]
        iHistorico.usuario= Usuario.objects.all()[0]
        iHistorico.data= str(datetime.datetime.today())[:19]
        iHistorico.empresa= Empresa.objects.all()[0]
        iHistorico.save()
        self.assertEquals(4, Historico.objects.count())
    
    def testSalvaHistorico(self):
        iIDVersao= Versao.objects.all()[0].id_versao
        iIDTipoEvento= Tipo_de_Evento.objects.all()[0].id_tipo_evento
        iIDUsuario= Usuario.objects.all()[0].id
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        iHistorico= Historico().salvaHistorico(iIDVersao, iIDTipoEvento, iIDUsuario, iIDEmpresa)
        self.assertEquals(4, Historico.objects.count())
        self.assertEquals(iIDEmpresa, iHistorico.empresa.id_empresa) 
    
    def testObtemListaDeEventos(self):
        iIDVersao= Versao.objects.all()[0].id_versao
        iListaEventos= Historico().obtemListaEventos(iIDVersao)
        self.assertEquals(3, len(iListaEventos))
    
    def testCalculaQuantidadeDeVisualizacoesDoDocumento(self):
        iVersao= Versao.objects.all()[0]
        iQuantidade= Historico().calculaQuantidadeDeVisualizacoesDoDocumento(iVersao)
        self.assertEquals(1, iQuantidade)
    
    def testCalculaQuantidadeDeDownloadsDoDocumento(self):
        iVersao= Versao.objects.all()[0]
        iQuantidade= Historico().calculaQuantidadeDeDownloadsDoDocumento(iVersao)
        self.assertEquals(1, iQuantidade)
        
#-----------------------------------------------------MOKS---------------------------------------------------  
    
    def mokarEmpresa(self):
        iNome           = 'empresa_001'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa_1      = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_1.save(False)
        
        iNome           = 'empresa_002'
        iPastaRaiz      = '/documentos/empresa_002/2'
        iEh_Ativo       = True
        iEmpresa_2      = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_2.save(False)
        
    def mokarTipoUsuario(self):
        iDescricacao= 'Tipo teste'
        iTipoUsuario= Tipo_de_Usuario()
        iTipoUsuario.descricao= iDescricacao
        iTipoUsuario.save()
        
    def mokarUsuario(self):
        iEmpresa_1      = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario    = Tipo_de_Usuario.objects.all()[0]
        iEmail          = 'usuario1@teste.com.br'
        iUsuario_1      = Usuario(empresa= iEmpresa_1, email= iEmail, tipo_usuario= iTipoUsuario)
        iUsuario_1.save()
        
    def mokarPasta(self):
        iNome            = 'Modelo'
        iDiretorio       = '/'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iPasta           = Pasta(nome= iNome, diretorio= iDiretorio, empresa= iEmpresa)
        iPasta.save()
        
    def mokarTipoDocumento(self):
        iDescricao      = 'Modelo'
        iEh_Nativo      = True
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento  = Tipo_de_Documento(descricao= iDescricao, eh_nativo= iEh_Nativo, empresa= iEmpresa)
        iTipoDocumento.save()
    
    def mokarMultiUploader(self):
        iUpload                 = MultiuploaderImage()
        iUpload.iFileName       = 'teste.txt'
        iUpload.iImage          = '/documento/teste.txt'
        iUpload.iKeyData        = iUpload.key_generate
        iUpload.iUploadDate     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iEmpresa                = Empresa.objects.filter(id_empresa=1)[0]
        iIDPasta                = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0].id_pasta
        iUpload.save(iIDPasta, iEmpresa.id_empresa)

    def mokarDocumento(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento  = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iPasta          = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iAssunto        = 'Teste'
        iEhPublico      = True
        iDocumento      = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento.save()
        
    def mokarEstadoVersao(self):
        iDescricao      = 'Disponivel'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
    
    def mokarCriarVersao(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iDocumento      = Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iEstado         = Estado_da_Versao.objects.filter()[0]
        iVersao         = 1
        iUpload         = MultiuploaderImage.objects.filter()[0]
        iDataCriacao    = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iEh_Assinado    = False
        iEh_Versao_Atual= True
        iVersao         = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao.save()
    
    def mokarTipoDeEvento(self):
        for i in range(7):
            iTipoDeEvento1= Tipo_de_Evento()
            iTipoDeEvento1.descricao= 'Evento mock %s' % str(i)
            iTipoDeEvento1.save()
    
    def mokarEventos(self):
        iIDVersao= Versao.objects.all()[0].id_versao
        iIDTipoEvento= Tipo_de_Evento.objects.all()[0].id_tipo_evento
        iIDUsuario= Usuario.objects.all()[0].id
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        Historico().salvaHistorico(iIDVersao, iIDTipoEvento, iIDUsuario, iIDEmpresa)
        
        iIDVersao= Versao.objects.all()[0].id_versao
        iIDTipoEvento= constantes.cntEventoHistoricoVisualizar
        iIDUsuario= Usuario.objects.all()[0].id
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        Historico().salvaHistorico(iIDVersao, iIDTipoEvento, iIDUsuario, iIDEmpresa)
        
        iIDVersao= Versao.objects.all()[0].id_versao
        iIDTipoEvento= constantes.cntEventoHistoricoDownload
        iIDUsuario= Usuario.objects.all()[0].id
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        Historico().salvaHistorico(iIDVersao, iIDTipoEvento, iIDUsuario, iIDEmpresa)
