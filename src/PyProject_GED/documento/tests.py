# -*- coding: utf-8 -*-
from django.test                                import TestCase

from autenticacao.models                        import Empresa #@UnresolvedImport
from autenticacao.models                        import Usuario #@UnresolvedImport
from seguranca.models                           import Pasta #@UnresolvedImport
from multiuploader.models                       import MultiuploaderImage #@UnresolvedImport

from models                                     import Tipo_de_Documento
from models                                     import Documento
from models                                     import Estado_da_Versao
from models                                     import Versao

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
        pass
    
    
    def tearDown(self):
        Versao.objects.all().delete()
        Estado_da_Versao.objects.all().delete()
        Documento.objects.all().delete()
        MultiuploaderImage.objects.all().delete()
        Tipo_de_Documento.objects.all().delete()
        Pasta.objects.all().delete()
        Usuario.objects.all().delete()
        Empresa.objects.all().delete()
        pass
    
    
    def testCriarTipoDocumento(self):
        iDescricao      = 'Modelo'
        iEh_Nativo      = True
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento  = Tipo_de_Documento(descricao= iDescricao, eh_nativo= iEh_Nativo, empresa= iEmpresa)
        iTipoDocumento.save()
        self.assertEquals(iTipoDocumento.id_tipo_documento, (Tipo_de_Documento.objects.filter
                                                             (empresa= iEmpresa.id_empresa).filter
                                                             (id_tipo_documento= 2)[0].id_tipo_documento))
    
    def testCriandoTipoDeDocumento(self):
        iEmpresa= Empresa.objects.all()[0]
        iDescricao= 'teste'
        iTipoDocumento= Tipo_de_Documento().criaTipoDocumento(iEmpresa, iDescricao)
        self.assertEquals(iDescricao, iTipoDocumento.descricao)
        
    def tetsObtemIDTipoDocumento(self):
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        iDescricaoTipoDocumento= 'Modelo'
        iIDTipoDocumento= Tipo_de_Documento().obtemIDTipoDocumento(iIDEmpresa, iDescricaoTipoDocumento)
        self.assertEquals(1, iIDTipoDocumento)
        
    def testObtemListaTipoDocumentoDaEmpresa(self):
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        iLista= Tipo_de_Documento().obtemListaTipoDocumentoDaEmpresa(iIDEmpresa)
        iListaTipoDocumento= Tipo_de_Documento.objects.filter(empresa= iIDEmpresa)
        self.assertEquals(len(iLista), len(iListaTipoDocumento))
        self.assertEquals(iLista[0].empresa, iListaTipoDocumento[0].empresa)
    
    def testObtemInformacoesDoDocumento(self):
        iIDVersao= Versao.objects.all()[0].id_versao
        iDocumento= Documento().obtemInformacoesDocumento(iIDVersao)
        self.assertEquals('Teste', iDocumento.assunto)
    
    def testCriarEstadoVersao(self):
        iDescricao      = 'Disponivel'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        self.assertEquals(iEstadoVersao.id_estado_da_versao, Estado_da_Versao.objects.filter(id_estado_da_versao=2)[0].id_estado_da_versao)
    
    def testCriaEstadoDaVersao(self):
        iDescricao= 'Bloqueado'
        iEstadoDaVersao= Estado_da_Versao().criaEstadoVersao(iDescricao)
        self.assertEquals(iDescricao, iEstadoDaVersao.descricao)
    
    def testObtemListaDeDocumentosDaPasta(self):
        iIDEmpresa= Empresa.objects.filter(id_empresa=1)[0].id_empresa
        iIDPasta= Pasta.objects.filter(empresa= iIDEmpresa)[0].id_pasta
        iLista= Versao().obtemListaDeDocumentosDaPasta(iIDEmpresa, iIDPasta)
        
        self.assertEquals(4, len(iLista))
    
    def testObtemListaDeVersoesDoDocumento(self):
        iIDVersao= Versao.objects.all()[0].id_versao
        iLista= Versao().obtemListaDeVersoesDoDocumento(iIDVersao)
        self.assertEquals(1, len(iLista))
        
    def testSalvaVersao(self):
        iIDDocumento= Documento.objects.all()[0].id_documento
        iIDCriador= Usuario.objects.all()[0].id
        iIDEstado= Estado_da_Versao.objects.all()[0].id_estado_da_versao
        iVersao= 1
        iUpload= MultiuploaderImage.objects.all()[0].key_data
        iProtocolo= '123'
        iVersao= Versao().salvaVersao(iIDDocumento, iIDCriador, iIDEstado, iVersao, iUpload, iProtocolo)
        self.assertEquals(iProtocolo, iVersao.protocolo)
        
    def testCriarDocumento(self):
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
        self.assertEquals(iDocumento.id_documento, Documento.objects.filter(empresa= iEmpresa.id_empresa).filter(id_documento= 5)[0].id_documento)
    
    def testSalvaDocumento(self):
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        iIDTipoDocumento= Tipo_de_Documento.objects.all()[0].id_tipo_documento
        iIDPasta= Pasta.objects.all()[0].id_pasta
        iAssunto= 'Doc Teste'
        iEhPublico= False
        iUsuarioResponsavel= Usuario.objects.all()[0]
        iDocumento= Documento().salvaDocumento(iIDEmpresa, iIDTipoDocumento, iIDPasta, iAssunto, iEhPublico, iUsuarioResponsavel)
        self.assertEquals(iAssunto, iDocumento.assunto)
    
    def testBuscaTodosOsDocumentos(self):
        iLista= Versao().buscaDocumentos()
        self.assertEquals(4, len(iLista))
    
    def testBuscaDocumentosPorAssunto(self):
        iAssunto1= 'Alpha'
        iAssunto2= 'Documento'
        iAssunto3= 'documento'
        iAssunto4= 'Propagação'
        
        iLista= Versao().buscaDocumentos(vAssunto= iAssunto1)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(vAssunto=iAssunto2)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(vAssunto=iAssunto3)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(vAssunto=iAssunto3)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(vAssunto=iAssunto4)
        self.assertEquals(0, len(iLista))
    
    def testBuscaDocumentosPorProtocolo(self):
        iProtocolo1= '1000'
        iProtocolo2= '1001'
        iProtocolo3= '10'
        
        iLista= Versao().buscaDocumentos(vProtocolo= iProtocolo1)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(vProtocolo= iProtocolo2)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(vProtocolo= iProtocolo3)
        self.assertEquals(0, len(iLista))
    
    def testBuscaDocumentosComMultiplosFiltros(self):
        iAssunto1= 'Alpha'
        iAssunto2= 'Documento'
        iAssunto3= 'documento'
        iProtocolo1= '1000'
        iProtocolo2= '1001'
        iProtocolo3= '1002'
        
        iLista= Versao().buscaDocumentos(vAssunto=iAssunto1, vProtocolo= iProtocolo1)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(vAssunto=iAssunto2, vProtocolo= iProtocolo2)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(vAssunto=iAssunto3, vProtocolo= iProtocolo3)
        self.assertEquals(1, len(iLista))
    
    def testCriarVersao(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iDocumento      = Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iEstado         = Estado_da_Versao.objects.filter()[0]
        iVersao         = 1
        iUpload         = MultiuploaderImage.objects.filter()[0]
        iDataCriacao    = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iEh_Assinado    = False
        iVersao         = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado)
        iVersao.save()
        self.assertEquals(iVersao.id_versao, Versao.objects.filter(id_versao= iVersao.id_versao)[0].id_versao)
    
    def testObtemVersaoAtualDoDocumento(self):
        iDocumento= Documento.objects.all()[0]
        iVersaAtual= Versao().obtemVersaoAtualDoDocumento(iDocumento)
        self.assertEquals(1, iVersaAtual.id_versao)
    
    def testObtemEstadosDaEmpresa(self):
        iListaDeEstados= Estado_da_Versao().obtemEstadosDaVersao()
        self.assertEquals(1, len(iListaDeEstados))
        
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
        
    def mokarUsuario(self):
        iEmpresa_1      = Empresa.objects.filter(id_empresa= 1)[0]
        iUsuario_1      = Usuario(empresa= iEmpresa_1)
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
        
        iDocumento1     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento1.save()
        
        iAssunto        = 'Documento Alpha'
        iDocumento2     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento2.save()
        
        iAssunto        = 'Documento Beta'
        iDocumento3     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento3.save()
        
        iAssunto        = 'Documentação'
        iDocumento4     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento4.save()
        
    def mokarEstadoVersao(self):
        iDescricao      = 'Disponivel'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
    
    def mokarCriarVersao(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iEstado         = Estado_da_Versao.objects.filter()[0]
        iVersao         = 1
        iUpload         = MultiuploaderImage.objects.filter()[0]
        
        iDocumento      = Documento.objects.filter(id_documento= 1)[0]
        iProtocolo      = '1001'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo)
        
        iDocumento      = Documento.objects.filter(id_documento= 2)[0]
        iProtocolo      = '1002'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo)
        
        iDocumento      = Documento.objects.filter(id_documento= 3)[0]
        iProtocolo      = '1003'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo)
        
        iDocumento      = Documento.objects.filter(id_documento= 4)[0]
        iProtocolo      = '1004'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo)
    
