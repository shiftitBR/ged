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
from PyProject_GED.workflow.models import Pendencia

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
        self.mokarcriaPendencia()
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

    def testcriaPendencia(self):
        iRemetente                  = Usuario.objects.all()[0]
        iDestinatario               = Usuario.objects.all()[1]
        iVersao                     = Versao.objects.all()[0]
        iPendencia                  = Pendencia()
        iPendencia.usr_remetente    = iRemetente
        iPendencia.usr_destinatario = iDestinatario
        iPendencia.versao           = iVersao   
        iPendencia.data             = datetime.datetime(2012, 02, 15, 15, 10, 45)    
        iPendencia.descricao        = 'descricao'
        iPendencia.save()
        self.assertEquals(2, iPendencia.id_pendencia)
        

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
        iPasta.save()
        
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
        
        
    def mokarcriaPendencia(self):
        iRemetente                  = Usuario.objects.all()[0]
        iDestinatario               = Usuario.objects.all()[1]
        iVersao                     = Versao.objects.all()[0]
        iPendencia                  = Pendencia()
        iPendencia.usr_remetente    = iRemetente
        iPendencia.usr_destinatario = iDestinatario
        iPendencia.versao           = iVersao   
        iPendencia.data             = datetime.datetime(2012, 02, 15, 15, 10, 45)    
        iPendencia.descricao        = 'descricao'
        iPendencia.save()