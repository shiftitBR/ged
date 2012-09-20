# -*- coding: utf-8 -*-
from django.test                                import TestCase
from django.conf                                import settings

from autenticacao.models                        import Empresa #@UnresolvedImport
from PyProject_GED.autenticacao.models          import Usuario, Tipo_de_Usuario
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
from PyProject_GED import constantes
from PyProject_GED.qualidade.models import Tipo_de_Norma, Norma, Norma_Documento

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
        self.mokarTipoIndice()
        self.mokarIndice()
        self.mokarAssociacaoIndiceVersao()
        self.mokarTipoNorma()
        self.mokarNorma()
        self.mokarAssociacaoNormaDocumento()
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
        Tipo_de_Usuario.objects.all().delete()
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
        
        self.assertEquals(7, len(iLista))
    
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
        self.assertEquals(iDocumento.id_documento, Documento.objects.filter(empresa= iEmpresa.id_empresa).filter(id_documento= 8)[0].id_documento)
    
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
        self.assertEquals(7, len(iLista))
    
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
        self.assertEquals(4, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3)
        self.assertEquals(4, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3)
        self.assertEquals(4, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto4)
        self.assertEquals(0, len(iLista))
    
    def testBuscaDocumentosPorProtocolo(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iProtocolo1= '1000'
        iProtocolo2= '1001'
        iProtocolo3= '0000001001'
        iProtocolo4= '10'
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vProtocolo= iProtocolo1)
        self.assertEquals(0, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vProtocolo= iProtocolo2)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vProtocolo= iProtocolo3)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vProtocolo= iProtocolo4)
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
        self.assertEquals(7, len(iLista))
    
    def testBuscaDocumentosPorEstadoDoDocumento(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iEstadoDoDocumento1= str(Estado_da_Versao.objects.all()[0].id_estado_da_versao)
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDEstadoDoDocumento= iEstadoDoDocumento1)
        self.assertEquals(7, len(iLista))
    
    def testBuscaDocumentosPorDataDeCriacao(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iDataInicial1= ControleDocumentos().formataData('01/08/2012')
        iDataFinal1= ControleDocumentos().formataData('05/08/2012')
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vDataDeCriacaoInicial= iDataInicial1)
        self.assertEquals(4, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vDataDeCriacaoInicial= iDataInicial1, vDataDeCriacaoFinal= iDataFinal1)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vDataDeCriacaoFinal= iDataFinal1)
        self.assertEquals(5, len(iLista))
    
    def testBuscaDocumentosPorIndicePersonalizadoTipoString(self):
        iEmpresa= Empresa.objects.filter(id_empresa=1)[0]
        iIDEmpresa= iEmpresa.id_empresa
        iIndice1= (1, 'TEste_stRIng1') #(id_indice, valor)
        iIndice2= (2, 'teste_string2')
        iIndice3= (2, 'teste_string1')
        iIndice4= (2, 'teste')
        
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
        
        iListaIndice= [] 
        iListaIndice.append(iIndice4)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vListaIndice= iListaIndice)
        self.assertEquals(0, len(iLista))
    
    def testBuscaDocumentosPorConteudo(self):
        iIDEmpresa= Empresa.objects.filter(id_empresa=1)[0].id_empresa
        iConteudo1= u'FrED'
        iConteudo2= u'RaPOsa'
        iConteudo3= u'Marisco'
        
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vConteudo= iConteudo1)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vConteudo= iConteudo2)
        self.assertEquals(2, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vConteudo= iConteudo3)
        self.assertEquals(0, len(iLista))
        
    def testBuscaDocumentosPorNorma(self):
        iIDEmpresa= Empresa.objects.filter(id_empresa=1)[0].id_empresa
        iNorma= Norma.objects.all()[0]    
        iLista= Versao().buscaDocumentos(iIDEmpresa, vItemNorma= iNorma)  
        self.assertEquals(1, len(iLista)) 
    
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
        iConteudo1= u'RaPOsa'
        iConteudo2= u'Marisco'
        iNorma= Norma.objects.all()[0]   
        
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
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3, vProtocolo= iProtocolo3, 
                                         vIDUsuarioCriador= iUsuarioCriador1, 
                                         vIDTipoDocumento= iTipoDocumento1, vConteudo= iConteudo2 )
        self.assertEquals(0, len(iLista))
        
        iListaIndice= [] 
        iListaIndice.append(iIndice2)
        iLista= Versao().buscaDocumentos(iIDEmpresa, vIDUsuarioCriador= iUsuarioCriador1, 
                                         vProtocolo= iProtocolo3, vIDTipoDocumento= iTipoDocumento1,
                                         vIDEstadoDoDocumento= iEstadoDoDocumento1, vListaIndice= iListaIndice,
                                         vConteudo= iConteudo1)
        self.assertEquals(1, len(iLista))
        
        iLista= Versao().buscaDocumentos(iIDEmpresa, vAssunto=iAssunto3, vProtocolo= iProtocolo3)
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
        
    def testgerarProtocolo(self):
        iDocumento  = Documento.objects.all()[0]
        iDocumento  = str('%07d'%iDocumento.id_documento)
        iVersao     = str('%03d'%1)
        iProtocolo  = '%s%s' %(iDocumento, iVersao)
        self.assertEquals('0000001001', iProtocolo)
    
    def testBuscaDocumentosPorVencimento(self):
        iDataAtual= ControleDocumentos().formataData('05/08/2012')
        iDocumentos= Documento().buscaDocumentosVencendo(iDataAtual)
        self.assertEquals(1, len(iDocumentos))
        
        iDataAtual= datetime.datetime.today()
        iDocumentos= Documento().buscaDocumentosVencendo(iDataAtual, 0)
        self.assertEquals(1, len(iDocumentos))
        
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
        iEmpresa       = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario   = Tipo_de_Usuario.objects.all()[0]
        
        iEmail          = 'usuario1@teste.com.br'
        iUsuario_1      = Usuario(empresa= iEmpresa, email= iEmail, tipo_usuario= iTipoUsuario)
        iUsuario_1.save()
        
        iEmail          = 'usuario2@teste.com.br'
        iUsuario_2      = Usuario(empresa= iEmpresa, email= iEmail, tipo_usuario= iTipoUsuario)
        iUsuario_2.save()
        
    def mokarPasta(self):
        iNome            = 'Modelo'
        iDiretorio       = '/'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iPasta           = Pasta(nome= iNome, diretorio= iDiretorio, empresa= iEmpresa)
        iPasta.save(False)
        
    def mokarTipoDocumento(self):
        iDescricao      = 'Modelo'
        iEh_Nativo      = True
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento  = Tipo_de_Documento(descricao= iDescricao, eh_nativo= iEh_Nativo, empresa= iEmpresa)
        iTipoDocumento.save()
    
    def mokarMultiUploader(self):
        iEmpresa                 = Empresa.objects.filter(id_empresa=1)[0]
        iIDPasta                 = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0].id_pasta
        
        iUpload1                 = MultiuploaderImage()
        iUpload1.filename        = 'teste.txt'
        iUpload1.image           = '%s/media_teste/teste.txt' % settings.MEDIA_ROOT
        iUpload1.key_data        = iUpload1.key_generate
        iUpload1.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload1.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload2                 = MultiuploaderImage()
        iUpload2.key_data        = iUpload2.key_generate
        iUpload2.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload2.filename        = 'texto.pdf'
        iUpload2.image           = '%s/media_teste/texto.pdf' % settings.MEDIA_ROOT
        iUpload2.save(iIDPasta, iEmpresa.id_empresa)
    
        iUpload3                 = MultiuploaderImage()
        iUpload3.key_data        = iUpload3.key_generate
        iUpload3.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload3.filename        = 'imagem_bmp.bmp'
        iUpload3.image           = '%s/media_teste/imagem_bmp.bmp' % settings.MEDIA_ROOT
        iUpload3.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload4                 = MultiuploaderImage()
        iUpload4.key_data        = iUpload4.key_generate
        iUpload4.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload4.filename        = 'texto.docx'
        iUpload4.image           = '%s/media_teste/texto.docx' % settings.MEDIA_ROOT
        iUpload4.save(iIDPasta, iEmpresa.id_empresa)

    def mokarDocumento(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento  = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iPasta          = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iAssunto        = 'Teste'
        iDataVencimento = ControleDocumentos().formataData('10/08/2012')
        iEhPublico      = True
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[0]
        iDocumento1     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    data_validade= iDataVencimento, eh_publico= iEhPublico)
        iDocumento1.save()
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[0]
        iAssunto        = 'Documento Alpha'
        iDataVencimento = datetime.datetime.today()
        iDocumento2     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    data_validade= iDataVencimento, eh_publico= iEhPublico)
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
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[1]
        iAssunto        = 'Documento PDF'
        iDocumento5     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento5.save()
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[1]
        iAssunto        = 'Imagem BMP'
        iDocumento6     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento6.save()
        
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[1]
        iAssunto        = 'Documento DOCX'
        iDocumento7     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento7.save()
        
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
        iProtocolo      = '0000001001'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iUpload         = MultiuploaderImage.objects.filter()[2]
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iDocumento      = Documento.objects.filter(id_documento= 2)[0]
        iProtocolo      = '0000001002'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iUpload         = MultiuploaderImage.objects.filter()[0]
        iDataCriacao    = ControleDocumentos().formataData('03/09/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 3)[0]
        iProtocolo      = '0000001003'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iDataCriacao    = ControleDocumentos().formataData('03/07/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 4)[0]
        iProtocolo      = '0000001004'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 5)[0]
        iProtocolo      = '0000001005'
        iUpload         = MultiuploaderImage.objects.all()[1]
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iDataCriacao    = ControleDocumentos().formataData('03/09/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 6)[0]
        iProtocolo      = '0000001006'
        iUpload         = MultiuploaderImage.objects.all()[2]
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iDataCriacao    = ControleDocumentos().formataData('03/07/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 7)[0]
        iProtocolo      = '0000001007'
        iUpload         = MultiuploaderImage.objects.all()[3]
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
    
    def mokarTipoIndice(self):
        iDescricao      = 'string'
        iTipoIndice     = Tipo_de_Indice(descricao= iDescricao)
        iTipoIndice.save()   
        
        
    def mokarIndice(self):
        iTipo           = Tipo_de_Indice.objects.all()[0]
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
        iValor          = 'teSTe_StrinG2'
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
        
    def mokarTipoNorma(self):
        iDescricao       = 'ABNT'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoNorma       = Tipo_de_Norma(descricao= iDescricao, empresa=iEmpresa)
        iTipoNorma.save()
        
    def mokarNorma(self):
        iEmpresa            = Empresa.objects.filter(id_empresa= 1)[0]
        iNorma= Norma()
        iNorma.tipo_norma   = Tipo_de_Norma.objects.filter(empresa= iEmpresa)[0]
        iNorma.empresa      = iEmpresa
        iNorma.descricao    = 'descricao norma'
        iNorma.norma_pai    = None
        iNorma.save()
    
    def mokarAssociacaoNormaDocumento(self):
        iNorma           = Norma.objects.filter(empresa= 1)[0]
        iDocumento       = Documento.objects.filter(empresa= 1)[2]
        iNormaDocumento  = Norma_Documento(norma= iNorma, documento= iDocumento)
        iNormaDocumento.save()