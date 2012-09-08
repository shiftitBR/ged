# -*- coding: utf-8 -*-
from django.test                                import TestCase
from django.conf                                import settings

from autenticacao.models                        import Empresa #@UnresolvedImport
from PyProject_GED.autenticacao.models          import Usuario, Tipo_de_Usuario
from seguranca.models                           import Pasta #@UnresolvedImport
from multiuploader.models                       import MultiuploaderImage #@UnresolvedImport

from PyProject_GED.documento.models             import Tipo_de_Documento
from PyProject_GED.documento.models             import Documento
from PyProject_GED.documento.models             import Estado_da_Versao
from PyProject_GED.documento.models             import Versao
from PyProject_GED.documento.controle           import Controle as ControleDocumentos

import datetime
from PyProject_GED.workflow.models import Pendencia, Tipo_de_Pendencia, Workflow,\
    Etapa_do_Workflow, Estado_da_Pendencia
from PyProject_GED.seguranca.models import Grupo, Grupo_Usuario
from PyProject_GED import constantes

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
        self.mokarGrupo()
        self.mokarGrupo_Usuario()
        self.mokarCriaWorkflow()
        self.mokarEstadoDaPendencia()
        self.mokarCriaTipoPendencia()
        self.mokarCriaEtapaDoWorkflow()
        self.mokarCriaPendencia()
        self.mokarCriaPendenciasDoWorkflow()
        pass
    
    
    def tearDown(self):
        Versao.objects.all().delete()
        Estado_da_Versao.objects.all().delete()
        Documento.objects.all().delete()
        MultiuploaderImage.objects.all().delete()
        Tipo_de_Documento.objects.all().delete()
        Pasta.objects.all().delete()
        Usuario.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Empresa.objects.all().delete()
        Pendencia.objects.all().delete()
        pass

    def testCriaPendencia(self):
        iRemetente                  = Usuario.objects.all()[0]
        iDestinatario               = Usuario.objects.all()[1]
        iVersao                     = Versao.objects.filter(id_versao= 1)[0]
        iTipoDePendencia            = Tipo_de_Pendencia.objects.all()[0]
        iPendencia= Pendencia().criaPendencia(iRemetente, iDestinatario, iVersao, 'descricao', iTipoDePendencia)
        self.assertEquals(5, iPendencia.id_pendencia)
        self.assertEquals('Pendente', Versao.objects.filter(id_versao= 1)[0].estado.descricao)
    
    def testCriaPendenciasDoWorkflow(self):
        iWorkflow= Workflow.objects.filter(id_workflow= 1)[0]
        iDocumento= Documento.objects.all()[0]
        iCriaPendencias= Pendencia().criaPendenciasDoWorkflow(iWorkflow, iDocumento)
        self.assertEquals(True, iCriaPendencias)
        self.assertEquals(6, Pendencia.objects.count())
    
    def testCancelaPendenciasDoWorkflow(self):
        iWorkflow= Workflow.objects.filter(id_workflow= 2)[0]
        iDocumento= Documento.objects.filter(id_documento= 2)[0]
        iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(Documento.objects.filter(id_documento= 2)[0])
        self.assertEquals(2, len(Pendencia.objects.filter(versao= iVersaoAtual, estado_da_pendencia= constantes.cntEstadoPendenciaPendente)))
        iCancelaPendencias= Pendencia().cancelaPendenciasDoWorkflow(iWorkflow, iDocumento)
        self.assertEquals(True, iCancelaPendencias)
        self.assertEquals(0, len(Pendencia.objects.filter(versao= iVersaoAtual, estado_da_pendencia= constantes.cntEstadoPendenciaPendente)))
    
    def testCriaTipoPendencia(self):
        iDescricao= 'Tipo de Pendencia'
        iTipoPendencia= Tipo_de_Pendencia()
        iTipoPendencia.descricao= iDescricao
        iTipoPendencia.save()
        self.assertEquals(3, Tipo_de_Pendencia.objects.count())
    
    def testConcluiPendencia(self):
        iPendencia= Pendencia.objects.all()[0]
        self.assertEquals(constantes.cntEstadoPendenciaPendente, iPendencia.estado_da_pendencia.id_estado_da_pendencia)
        
        iPendencia= Pendencia().concluiPendencia(iPendencia)
        self.assertEquals(constantes.cntEstadoPendenciaConcluida, iPendencia.estado_da_pendencia.id_estado_da_pendencia)
    
    def testCriaWorkflow(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoDocumento  = Tipo_de_Documento.objects.all()[0]
        iPasta          = Pasta.objects.all()[0]
        iDescricao      = 'Workflow'
        iWorkflow= Workflow(empresa= iEmpresa, tipo_de_documento= iTipoDocumento, pasta= iPasta, descricao= iDescricao)
        iWorkflow.save()
        self.assertEquals(3, Workflow.objects.count())
        
    def testCriaEtapaDoWorkflow(self):
        iWorkflow= Workflow.objects.filter(id_workflow= 1)[0]
        iGrupo= Grupo.objects.all()[0]
        iTipoDePendencia= Tipo_de_Pendencia.objects.all()[0]
        iEhMultiplo=  True
        iDescricao= 'Etapa 1'
        iEtapa= Etapa_do_Workflow(workflow= iWorkflow, grupo= iGrupo, tipo_de_pendencia= iTipoDePendencia, 
                                  eh_multipla= iEhMultiplo, descricao= iDescricao)
        iEtapa.save()
        self.assertEquals(5, Etapa_do_Workflow.objects.count())
    
    def testObtemWorkflow(self):
        iPasta= Pasta.objects.all()[0]
        iTipoDeDocumento= Tipo_de_Documento.objects.all()[0]
        iWorkflow= Workflow().obtemWorkflow(iPasta, iTipoDeDocumento)
        self.assertEquals(1, iWorkflow.id_workflow)
    
    def testObtemEtapaAtual(self):
        iWorkflow= Workflow.objects.all()[0]
        iEtapaAtual= Workflow().obtemEtapaAtual(iWorkflow)
        self.assertEquals(0, iEtapaAtual.ordem_da_etapa)
    
    def testObtemProximaEtapa(self):
        iWorkflow= Workflow.objects.all()[0]
        iProximaEtapa= Workflow().obtemProximaEtapa(iWorkflow)
        self.assertEquals(1, iProximaEtapa.ordem_da_etapa)
    
    def testVerificaSeEtapaAtualEstaConcluida(self):
        iWorkflow= Workflow.objects.all()[1]
        iEhConcluida= Workflow().verificaSeEtapaAtualEstaConcluida(iWorkflow)
        self.assertEquals(False, iEhConcluida)
        self.mokarConcluiPendencia()
        iEhConcluida= Workflow().verificaSeEtapaAtualEstaConcluida(iWorkflow)
        self.assertEquals(True, iEhConcluida)
    
    def testAlteraEstadoDoDocumentoDaPendencia(self):
        iWorkflow= Workflow.objects.all()[0]
        iEtapaAtual= Workflow().obtemEtapaAtual(iWorkflow)
        iDocumento= Documento.objects.filter(id_documento= 2)
        iEstado= Workflow().alteraEstadoDoDocumentoDoWorkflow(iEtapaAtual, iDocumento)
        iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(iDocumento)
        self.assertEquals(True, iEstado)
        self.assertEquals(constantes.cntEstadoVersaoAprovado, iVersaoAtual.estado.id_estado_da_versao)
    
    def testExecutandoWorkflow(self):
        iDocumento_SemWorkflow= Documento.objects.filter(id_documento= 3)[0]
        iDocumento_ComWorkflow= Documento.objects.filter(id_documento= 4)[0]
        
        self.assertEquals(4, Pendencia.objects.count())
        self.assertEquals(1, len(Pendencia.objects.filter(etapa_do_workflow= 1)))
        
        Workflow().executaWorkflow(iDocumento_SemWorkflow)
        self.assertEquals(4, Pendencia.objects.count())
        self.assertEquals(1, len(Pendencia.objects.filter(etapa_do_workflow= 1)))
        
        
        self.mokarCriaPendenciasDoWorkflow_2()
        iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(Documento.objects.filter(id_documento= 4)[0])
        self.assertEquals(2, len(Pendencia.objects.filter(versao= iVersaoAtual, estado_da_pendencia= constantes.cntEstadoPendenciaPendente)))
        self.assertEquals('Pendente', iVersaoAtual.estado.descricao)
        self.mokarConcluiPendencia_2()
        Workflow().executaWorkflow(iDocumento_ComWorkflow)
        
        iVersaoAtual= Versao().obtemVersaoAtualDoDocumento(Documento.objects.filter(id_documento= 4)[0])
        self.assertEquals(0, len(Pendencia.objects.filter(versao= iVersaoAtual, estado_da_pendencia= constantes.cntEstadoPendenciaPendente)))
        self.assertEquals('Aprovado', iVersaoAtual.estado.descricao)
        
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
        iTipoDocumento1  = Tipo_de_Documento(descricao= iDescricao, eh_nativo= iEh_Nativo, empresa= iEmpresa)
        iTipoDocumento1.save()
        
        iDescricao      = 'Contrato'
        iEh_Nativo      = False
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento2  = Tipo_de_Documento(descricao= iDescricao, eh_nativo= iEh_Nativo, empresa= iEmpresa)
        iTipoDocumento2.save()
        
        iDescricao      = 'Proposta'
        iEh_Nativo      = False
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento3  = Tipo_de_Documento(descricao= iDescricao, eh_nativo= iEh_Nativo, empresa= iEmpresa)
        iTipoDocumento3.save()
    
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
        iTipoDocumento  = Tipo_de_Documento.objects.filter(id_tipo_documento= 2)[0]
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
        
        iTipoDocumento2  = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)[2]
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[1]
        iAssunto        = 'Documento Beta'
        iDocumento3     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento2, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    eh_publico= iEhPublico)
        iDocumento3.save()
        
        iTipoDocumento3  = Tipo_de_Documento.objects.filter(id_tipo_documento= 1)[0]
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa)[1]
        iAssunto        = 'Documentação'
        iDocumento4     = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento3, 
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
        
        iDescricao      = 'Bloqueado'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        
        iDescricao      = 'Aprovado'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        
        iDescricao      = 'Reprovado'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        
        iDescricao      = 'Excluido'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        
        iDescricao      = 'Obsoleto'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        
        iDescricao      = 'Pendente'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        
        iDescricao      = 'Vencido'
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
        
        iUpload         = MultiuploaderImage.objects.filter()[2]
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iDocumento      = Documento.objects.filter(id_documento= 2)[0]
        iProtocolo      = '1002'
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iUpload         = MultiuploaderImage.objects.filter()[0]
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
        
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 5)[0]
        iProtocolo      = '1005'
        iUpload         = MultiuploaderImage.objects.all()[1]
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iDataCriacao    = ControleDocumentos().formataData('03/09/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 6)[0]
        iProtocolo      = '1006'
        iUpload         = MultiuploaderImage.objects.all()[2]
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
        iDataCriacao    = ControleDocumentos().formataData('03/07/2012')
        iCriador        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[1]
        iDocumento      = Documento.objects.filter(id_documento= 7)[0]
        iProtocolo      = '1007'
        iUpload         = MultiuploaderImage.objects.all()[3]
        Versao().salvaVersao(iDocumento.id_documento, iCriador.id, iEstado.id_estado_da_versao, 
                             iVersao, iUpload.key_data, iProtocolo, iDataCriacao)
        
    def mokarEstadoDaPendencia(self):
        iDescricao_1= 'Pendente'
        iDescricao_2= 'Concluido'
        iDescricao_3= 'Cancelada'
        iEstado_1   = Estado_da_Pendencia(descricao= iDescricao_1)  
        iEstado_1.save()
        iEstado_2   = Estado_da_Pendencia(descricao= iDescricao_2) 
        iEstado_2.save()
        iEstado_3   = Estado_da_Pendencia(descricao= iDescricao_3) 
        iEstado_3.save()
        
        
    def mokarCriaPendencia(self):
        iRemetente                  = Usuario.objects.all()[0]
        iDestinatario               = Usuario.objects.all()[1]
        iVersao                     = Versao.objects.all()[0]
        iTipoDePendencia            = Tipo_de_Pendencia.objects.all()[0]
        
        iPendencia_1                    = Pendencia()
        iPendencia_1.usr_remetente      = iRemetente
        iPendencia_1.usr_destinatario   = iDestinatario
        iPendencia_1.versao             = iVersao   
        iPendencia_1.data               = datetime.datetime(2012, 02, 15, 15, 10, 45)    
        iPendencia_1.descricao          = 'descricao 1'
        iPendencia_1.tipo_de_pendencia  = iTipoDePendencia
        iPendencia_1.save()
        
        iPendencia_2                    = Pendencia()
        iPendencia_2.usr_remetente      = iRemetente
        iPendencia_2.usr_destinatario   = iDestinatario
        iPendencia_2.versao             = iVersao   
        iPendencia_2.data               = datetime.datetime(2012, 02, 15, 15, 10, 45)    
        iPendencia_2.descricao          = 'descricao 2'
        iPendencia_2.tipo_de_pendencia  = Tipo_de_Pendencia.objects.filter(id_tipo_de_pendencia= constantes.cntTipoPendenciaAprovacao)[0]
        iPendencia_2.workflow           = Workflow.objects.all()[0]
        iPendencia_2.etapa_do_workflow  = Etapa_do_Workflow.objects.all()[0]
        iPendencia_2.save()
    
    def mokarCriaTipoPendencia(self):
        iDescricao= 'Aprovacao'
        iTipoPendencia= Tipo_de_Pendencia()
        iTipoPendencia.descricao= iDescricao
        iTipoPendencia.save()
        
        iDescricao= 'Assinatura'
        iTipoPendencia= Tipo_de_Pendencia()
        iTipoPendencia.descricao= iDescricao
        iTipoPendencia.save()
    
    def mokarCriaWorkflow(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iPasta          = Pasta.objects.filter(empresa= iEmpresa)[0]
        
        iTipoDocumento  = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa, id_tipo_documento= 1)[0]
        iDescricao      = 'Workflow 1'
        iWorkflow1= Workflow(empresa= iEmpresa, tipo_de_documento= iTipoDocumento, pasta= iPasta, descricao= iDescricao)
        iWorkflow1.save()
        
        iTipoDocumento  = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa, id_tipo_documento= 2)[0]
        iDescricao      = 'Workflow 2'
        iWorkflow2= Workflow(empresa= iEmpresa, tipo_de_documento= iTipoDocumento, pasta= iPasta, descricao= iDescricao)
        iWorkflow2.save()
    
    def mokarCriaEtapaDoWorkflow(self):
        iWorkflow1= Workflow.objects.filter(id_workflow= 1)[0]
        iGrupo= Grupo.objects.all()[0]
        iTipoDePendencia= Tipo_de_Pendencia.objects.all()[0]
        iEhMultiplo= True
        
        iDescricao_1= 'Etapa 1'
        iEtapa_1= Etapa_do_Workflow(workflow= iWorkflow1, grupo= iGrupo, tipo_de_pendencia= iTipoDePendencia, 
                                  eh_multipla= iEhMultiplo, descricao= iDescricao_1)
        iEtapa_1.save()
        
        iDescricao_2= 'Etapa 2'
        iEtapa_2= Etapa_do_Workflow(workflow= iWorkflow1, grupo= iGrupo, tipo_de_pendencia= iTipoDePendencia, 
                                  eh_multipla= iEhMultiplo, descricao= iDescricao_2)
        iEtapa_2.save()
        
        iWorkflow2= Workflow.objects.filter(id_workflow= 2)[0]
        iGrupo= Grupo.objects.all()[0]
        iTipoDePendencia= Tipo_de_Pendencia.objects.all()[0]
        iEhMultiplo=  False
        
        iDescricao_1= 'Etapa 1'
        iEtapa_1= Etapa_do_Workflow(workflow= iWorkflow2, grupo= iGrupo, tipo_de_pendencia= iTipoDePendencia, 
                                  eh_multipla= iEhMultiplo, descricao= iDescricao_1)
        iEtapa_1.save()
        
        iDescricao_2= 'Etapa 2'
        iEtapa_2= Etapa_do_Workflow(workflow= iWorkflow2, grupo= iGrupo, tipo_de_pendencia= iTipoDePendencia, 
                                  eh_multipla= iEhMultiplo, descricao= iDescricao_2)
        iEtapa_2.save()

    def mokarGrupo(self):
        iNome            = 'Teste'
        iDescricao       = 'Colaboradores'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupo           = Grupo(nome= iNome, descricao= iDescricao, empresa= iEmpresa)
        iGrupo.save()
    
    def mokarGrupo_Usuario(self):
        iEmpresa               = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupo_Usuario1        = Grupo_Usuario()
        iGrupo_Usuario1.grupo  = Grupo.objects.filter(empresa= 1)[0]
        iGrupo_Usuario1.usuario= Usuario.objects.filter(empresa= iEmpresa)[0]
        iGrupo_Usuario1.save()
        
        iGrupo_Usuario2        = Grupo_Usuario()
        iGrupo_Usuario2.grupo  = Grupo.objects.filter(empresa= 1)[0]
        iGrupo_Usuario2.usuario= Usuario.objects.filter(empresa= iEmpresa)[1]
        iGrupo_Usuario2.save()
    
    def mokarCriaPendenciasDoWorkflow(self):
        iWorkflow= Workflow.objects.filter(id_workflow= 2)[0]
        iDocumento= Documento.objects.filter(id_documento= 2)[0]
        Pendencia().criaPendenciasDoWorkflow(iWorkflow, iDocumento)
    
    def mokarConcluiPendencia(self):
        iWorkflow= Workflow.objects.filter(id_workflow= 2)[0]
        iPendencia= Pendencia.objects.filter(workflow= iWorkflow)[0]
        iPendencia= Pendencia().concluiPendencia(iPendencia)
    
    def mokarCriaPendenciasDoWorkflow_2(self):
        iWorkflow= Workflow.objects.filter(id_workflow= 1)[0]
        iDocumento= Documento.objects.filter(id_documento= 4)[0]
        Pendencia().criaPendenciasDoWorkflow(iWorkflow, iDocumento)
    
    def mokarConcluiPendencia_2(self):
        iWorkflow= Workflow.objects.filter(id_workflow= 1)[0]
        iPendencia1= Pendencia.objects.filter(workflow= iWorkflow)[0]
        iPendencia2= Pendencia.objects.filter(workflow= iWorkflow)[1]
        Pendencia().concluiPendencia(iPendencia1)
        Pendencia().concluiPendencia(iPendencia2)
    