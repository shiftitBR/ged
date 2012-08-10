# -*- coding: utf-8 -*-
from django.test                                import TestCase

from autenticacao.models                        import Empresa #@UnresolvedImport
from PyProject_GED.autenticacao.models          import Usuario
from seguranca.models                           import Pasta #@UnresolvedImport
from multiuploader.models                       import MultiuploaderImage #@UnresolvedImport

from models                                     import Tipo_de_Documento
from models                                     import Documento
from models                                     import Estado_da_Versao
from models                                     import Versao
from controle                                   import Controle as ControleDocumentos

import datetime
from PyProject_GED.indice.models import Tipo_de_Indice, Indice,\
    Indice_Versao_Valor

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
        self.mokarAssociacaoIndiceVersao()
        pass
    
    
    def tearDown(self):
        Indice_Versao_Valor.objects.all().delete()
        Indice.objects.all().delete()
        Tipo_de_Indice.objects.all().delete()
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
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iLista= Versao().buscaDocumentos(iIDEmpresa)
        self.assertEquals(4, len(iLista))
    
    def testBuscaDocumentosPorAssunto(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iAssunto1= 'Alpha'
        iAssunto2= 'Documento'
        iAssunto3= 'documento'
        iAssunto4= 'Propagação'
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto= iAssunto1)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto2)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto4)
        self.assertEquals(0, len(iLista))
    
    def testBuscaDocumentosPorProtocolo(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iProtocolo1= '1000'
        iProtocolo2= '1001'
        iProtocolo3= '10'
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vProtocolo= iProtocolo1)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vProtocolo= iProtocolo2)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vProtocolo= iProtocolo3)
        self.assertEquals(0, len(iLista))
    
    def testBuscaDocumentosPorUsuarioResponsavel(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iUsuario1= str(Usuario.objects.filter(empresa= iEmpresa)[0].id)
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioResponsavel= iUsuario1)
        self.assertEquals(2, len(iLista))
    
    def testBuscaDocumentosPorUsuarioCriador(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iUsuario1= str(Usuario.objects.filter(empresa= iEmpresa)[0].id)
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioCriador= iUsuario1)
        self.assertEquals(2, len(iLista))
    
    def testBuscaDocumentosPorTipoDoDocumento(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iTipoDocumento1= Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)[0].id_tipo_documento
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDTipoDocumento= iTipoDocumento1)
        self.assertEquals(4, len(iLista))
    
    def testBuscaDocumentosPorEstadoDoDocumento(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iEstadoDoDocumento1= str(Estado_da_Versao.objects.all()[0].id_estado_da_versao)
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDEstadoDoDocumento= iEstadoDoDocumento1)
        self.assertEquals(4, len(iLista))
    
    def testBuscaDocumentosPorDataDeCriacao(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iDataInicial1= ControleDocumentos().formataData('01/08/2012')
        iDataFinal1= ControleDocumentos().formataData('05/08/2012')
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vDataDeCriacaoInicial= iDataInicial1)
        self.assertEquals(3, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vDataDeCriacaoInicial= iDataInicial1, vDataDeCriacaoFinal= iDataFinal1)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vDataDeCriacaoFinal= iDataFinal1)
        self.assertEquals(3, len(iLista))
    
    def testBuscaDocumentosPorIndicePersonalizadoTipoString(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iIndice1= (1, 'teste_string1') #(id_indice, valor)
        iIndice2= (2, 'teste_string2')
        iIndice3= (2, 'teste_string1')
        
        iListaIndice= [] 
        iListaIndice.append(iIndice1)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vListaIndice= iListaIndice)
        self.assertEquals(1, len(iLista))
        
        iListaIndice= [] 
        iListaIndice.append(iIndice1)
        iListaIndice.append(iIndice2)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vListaIndice= iListaIndice)
        self.assertEquals(1, len(iLista))
        
        iListaIndice= [] 
        iListaIndice.append(iIndice3)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vListaIndice= iListaIndice)
        self.assertEquals(0, len(iLista))
        
        iListaIndice= [] 
        iListaIndice.append(iIndice2)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vListaIndice= iListaIndice)
        self.assertEquals(4, len(iLista))
    
    def testBuscaDocumentosComMultiplosFiltros(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iAssunto1= 'Alpha'
        iAssunto2= 'Documento'
        iAssunto3= 'documento'
        iProtocolo1= '1000'
        iProtocolo2= '1001'
        iProtocolo3= '1002'
        iUsuarioResponsavel1=  str(Usuario.objects.filter(empresa= iEmpresa)[0].id)
        iUsuarioResponsavel2=  str(Usuario.objects.filter(empresa= iEmpresa)[1].id)
        iUsuarioCriador1=  str(Usuario.objects.filter(empresa= iEmpresa)[0].id)
        iUsuarioCriador2=  str(Usuario.objects.filter(empresa= iEmpresa)[1].id)
        iTipoDocumento1= str(Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)[0].id_tipo_documento)
        iEstadoDoDocumento1= str(Estado_da_Versao.objects.all()[0].id_estado_da_versao)
        iIndice2= (2, 'teste_string2')
        iIndice3= (2, 'teste_string1')
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto1, vProtocolo= iProtocolo1)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto2, vProtocolo= iProtocolo2)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3, vProtocolo= iProtocolo3)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioResponsavel= iUsuarioResponsavel1, 
                                         vProtocolo= iProtocolo3)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioResponsavel= iUsuarioResponsavel2, 
                                         vProtocolo= iProtocolo3)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioCriador= iUsuarioCriador1, 
                                         vProtocolo= iProtocolo3)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3, vProtocolo= iProtocolo3, 
                                         vIDUsuarioCriador= iUsuarioCriador2)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioCriador= iUsuarioCriador1, 
                                         vProtocolo= iProtocolo3, vIDTipoDocumento= iTipoDocumento1)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3, vProtocolo= iProtocolo3, 
                                         vIDUsuarioCriador= iUsuarioCriador1, 
                                         vIDTipoDocumento= iTipoDocumento1 )
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3, vProtocolo= iProtocolo3, 
                                         vIDUsuarioCriador= iUsuarioCriador2, 
                                         vIDTipoDocumento= iTipoDocumento1 )
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto2, vProtocolo= iProtocolo2,
                                         vIDEstadoDoDocumento= iEstadoDoDocumento1)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioCriador= iUsuarioCriador1, 
                                         vProtocolo= iProtocolo3, vIDTipoDocumento= iTipoDocumento1,
                                         vIDEstadoDoDocumento= iEstadoDoDocumento1)
        self.assertEquals(1, len(iLista))
        
        iListaIndice= [] 
        iListaIndice.append(iIndice3)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioCriador= iUsuarioCriador1, 
                                         vProtocolo= iProtocolo3, vIDTipoDocumento= iTipoDocumento1,
                                         vIDEstadoDoDocumento= iEstadoDoDocumento1, vListaIndice= iListaIndice)
        self.assertEquals(0, len(iLista))
        
        iListaIndice= [] 
        iListaIndice.append(iIndice2)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioCriador= iUsuarioCriador1, 
                                         vProtocolo= iProtocolo3, vIDTipoDocumento= iTipoDocumento1,
                                         vIDEstadoDoDocumento= iEstadoDoDocumento1, vListaIndice= iListaIndice)
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
        
    def testGerarProtocolo(self):
        iVersao     = Versao.objects.filter()[0]
        iAno        = str(datetime.datetime.year)
        iMes        = str(datetime.datetime.month)
        iDia        = str(datetime.datetime.day)
        iProtocolo  = '%s%s%s%s%s' %(iAno, iMes, iDia, str(iVersao.documento.id_documento), str(iVersao.id_versao))
        print iProtocolo
        
        
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
        iEmpresa       = Empresa.objects.filter(id_empresa= 1)[0]
        
        iEmail          = 'usuario1@teste.com.br'
        iUsuario_1      = Usuario(empresa= iEmpresa, email= iEmail)
        iUsuario_1.save()
        
        iEmail          = 'usuario2@teste.com.br'
        iUsuario_2      = Usuario(empresa= iEmpresa, email= iEmail)
        iUsuario_2.save()
        
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
        iUpload.filename        = 'teste.txt'
        iUpload.image           = '/documento/teste.txt'
        iUpload.key_data        = iUpload.key_generate
        iUpload.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
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
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[0]
        iAssunto        = 'Documento Alpha'
        iDocumento2     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento2.save()
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[1]
        iAssunto        = 'Documento Beta'
        iDocumento3     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento3.save()
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[1]
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
        iEstado         = Estado_da_Versao.objects.all()[0]
        iVersao         = 1
        iUpload         = MultiuploaderImage.objects.filter()[0]
        iDataCriacao    = ControleDocumentos().formataData('03/08/2012')
        
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iDocumento      = Documento.objects.filter(id_documento= 1)[0]
        iProtocolo      = '1001'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iDocumento      = Documento.objects.filter(id_documento= 2)[0]
        iProtocolo      = '1002'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iDataCriacao    = ControleDocumentos().formataData('03/09/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 3)[0]
        iProtocolo      = '1003'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iDataCriacao    = ControleDocumentos().formataData('03/07/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 4)[0]
        iProtocolo      = '1004'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
    
    def mokarTipoIndice(self):
        iDescricao      = 'string'
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]     
        iTipoIndice     = Tipo_de_Indice(descricao= iDescricao, empresa= iEmpresa)
        iTipoIndice.save()   
        
        
    def mokarIndice(self):
        iTipo           = Tipo_de_Indice.objects.filter(empresa= 1)[0]
        iEmpresa        = Empresa.objects.filter()[0]
        
        iDescricao      = 'nome'
        iIndice1        = Indice(descricao= iDescricao, tipo_indice= iTipo, empresa= iEmpresa)
        iIndice1.save()
        
        iDescricao      = 'qualidade'
        iIndice2        = Indice(descricao= iDescricao, tipo_indice= iTipo, empresa= iEmpresa)
        iIndice2.save()

    def mokarAssociacaoIndiceVersao(self):
        iIDIndice1       = Indice.objects.filter(id_indice= 1)[0].id_indice
        iIDIndice2       = Indice.objects.filter(id_indice= 2)[0].id_indice
        
        iIDVersao       = Versao.objects.filter(documento__id_documento= 1)[0].id_versao
        iValor          = 'teste_string1'
        Indice_Versao_Valor().salvaValorIndice(iValor, iIDIndice1, iIDVersao)
        
        iIDVersao       = Versao.objects.filter(documento__id_documento= 1)[0].id_versao
        iValor          = 'teste_string2'
        Indice_Versao_Valor().salvaValorIndice(iValor, iIDIndice2, iIDVersao)
        
        iIDVersao       = Versao.objects.filter(documento__id_documento= 2)[0].id_versao
        iValor          = 'teste_string2'
        Indice_Versao_Valor().salvaValorIndice(iValor, iIDIndice2, iIDVersao)
        
        iIDVersao       = Versao.objects.filter(documento__id_documento= 3)[0].id_versao
        iValor          = 'teste_string2'
        Indice_Versao_Valor().salvaValorIndice(iValor, iIDIndice2, iIDVersao)
        
        iIDVersao       = Versao.objects.filter(documento__id_documento= 4)[0].id_versao
        iValor          = 'teste_string2'
        Indice_Versao_Valor().salvaValorIndice(iValor, iIDIndice2, iIDVersao)