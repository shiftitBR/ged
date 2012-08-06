
from django.test                                import TestCase

from autenticacao.models                import Empresa #@UnresolvedImport
from documento.models                   import Versao   #@UnresolvedImport

from models                             import Tipo_de_Indice
from models                             import Indice
from models                             import Indice_Versao_Valor
from PyProject_GED.documento.models     import Tipo_de_Documento, Documento, Estado_da_Versao
from PyProject_GED.documento.controle   import Controle as ControleDocumentos
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.multiuploader.models import MultiuploaderImage
from PyProject_GED.seguranca.models     import Pasta

import datetime


class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarUsuario()
        self.mokarPasta()
        self.mokarTipoDocumento()
        self.mokarMultiUploader()
        self.mokarDocumento()
        self.mokarEstadoVersao()
        self.mokarCriarVersao()
        self.mokarTipoIndice()
        self.mokarIndice()
        pass
    
    
    def tearDown(self):
        Empresa.objects.all().delete()
        Tipo_de_Indice.objects.all().delete()
        Indice.objects.all().delete()
        pass
    
    
    def testCriarIndice(self):
        iDescricao      = 'valor'
        iTipo           = Tipo_de_Indice.objects.filter(empresa= 1)[0]
        iEmpresa        = Empresa.objects.filter()[0]
        iIndice         = Indice(descricao= iDescricao, tipo_indice= iTipo, empresa= iEmpresa)
        iIndice.save()
        self.assertEquals(iIndice.id_indice, (Indice.objects.filter(empresa= iEmpresa.id_empresa).filter(id_indice= 2)[0].id_indice))
    
    
    def testCriarIndiceVersaoValor(self):
        iIDIndice       = Indice.objects.filter(id_indice= 1)[0].id_indice
        iIDVersao       = Versao.objects.filter(documento__id_documento= 1)[0].id_versao
        iValor          = 'teste_string1'
        Indice_Versao_Valor().salvaValorIndice(iValor, iIDIndice, iIDVersao)
        self.assertEquals(1, Indice_Versao_Valor.objects.count())
        
    def testObterIDsDasVersoesFiltradasPorIndice(self):
        self.testCriarIndiceVersaoValor()
        iIDEmpresa= Empresa.objects.filter(id_empresa= 1)[0].id_empresa
        iValor= 'teste_string1'
        iIDIndice= Indice.objects.filter(id_indice= 1)[0].id_indice
        iListaIDsVersoes= Indice_Versao_Valor().obtemIDVersoesFiltradosPorIndice(iIDEmpresa, iIDIndice, iValor)
        self.assertEquals(1, len(iListaIDsVersoes))
        self.assertEquals(1, iListaIDsVersoes[0])
    
    #-----------------------------------------------------MOKS---------------------------------------------------
    
    
    def mokarTipoIndice(self):
        iDescricao      = 'string'
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]     
        iTipoIndice     = Tipo_de_Indice(descricao= iDescricao, empresa= iEmpresa)
        iTipoIndice.save()   
        
        
    def mokarEmpresa(self):
        iNome           = 'empresa_001'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa_1      = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_1.save(False)
    
    def mokarUsuario(self):
        iEmpresa       = Empresa.objects.filter(id_empresa= 1)[0]
        
        iEmail          = 'usuario1@teste.com.br'
        iUsuario_1      = Usuario(empresa= iEmpresa, email= iEmail)
        iUsuario_1.save()
        
    def mokarIndice(self):
        iDescricao      = 'valor'
        iTipo           = Tipo_de_Indice.objects.filter(empresa= 1)[0]
        iEmpresa        = Empresa.objects.filter()[0]
        iIndice         = Indice(descricao= iDescricao, tipo_indice= iTipo, empresa= iEmpresa)
        iIndice.save()
    
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
        iPasta          = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iAssunto        = 'Teste'
        iEhPublico      = True
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[0]
        iDocumento1     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento1.save()
        
    def mokarEstadoVersao(self):
        iDescricao      = 'Disponivel'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
    
    def mokarCriarVersao(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iEstado         = Estado_da_Versao.objects.all()[0]
        iVersao         = 1
        iUpload         = MultiuploaderImage.objects.filter()[0]
        iDataCriacao    = ControleDocumentos().formataData('03/08/2012')
        
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iDocumento      = Documento.objects.filter(id_documento= 1)[0]
        iProtocolo      = '1001'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)