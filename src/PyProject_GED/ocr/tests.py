'''
Created on Aug 6, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.test                            import TestCase
from controle                               import Controle as ControleOCR
from django.conf                            import settings
from PyProject_GED.autenticacao.models      import Empresa, Usuario
from PyProject_GED.seguranca.models         import Pasta
from PyProject_GED.documento.models         import Tipo_de_Documento, Documento, Estado_da_Versao, Versao
from PyProject_GED.multiuploader.models     import MultiuploaderImage

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

    
    def testOCRImagemTIFF(self):
        iIDVersao= Versao.objects.all()[0].id_versao
        iString= ControleOCR().obtemTextoDaImagem(iIDVersao)
        self.assertEquals(True, len(iString) > 0)
    
    def testOCRImagemJPEG(self):
        iIDVersao= Versao.objects.all()[1].id_versao
        iString= ControleOCR().obtemTextoDaImagem(iIDVersao)
        self.assertEquals(True, len(iString) > 0)
        
    def testOCRImagemPNG(self):
        iIDVersao= Versao.objects.all()[2].id_versao
        iString= ControleOCR().obtemTextoDaImagem(iIDVersao)
        self.assertEquals(True, len(iString) > 0)
          
    def testLerTextoDOC(self):
        iIDVersao= Versao.objects.all()[3].id_versao
        iTexto= 'Fred'
        iEncontrou= ControleOCR().buscaTextoNoDocumento(iIDVersao, iTexto)
        self.assertEquals(True, iEncontrou)
    
    def testLerTextoODT(self):
        iIDVersao= Versao.objects.all()[4].id_versao
        iTexto= 'FRED'
        iEncontrou= ControleOCR().buscaTextoNoDocumento(iIDVersao, iTexto)
        self.assertEquals(True, iEncontrou)
        
    def testLerTextoTXT(self):
        iIDVersao= Versao.objects.all()[5].id_versao
        iTexto= 'FRED'
        iEncontrou= ControleOCR().buscaTextoNoTXT(iTexto, vIDVersao= iIDVersao)
        self.assertEquals(True, iEncontrou)
    
    def testLerTextoPDF(self):
        iIDVersao= Versao.objects.all()[6].id_versao
        iTexto= 'FRED'
        iEncontrou= ControleOCR().buscaTextoNoPDF(iIDVersao, iTexto)
        self.assertEquals(True, iEncontrou)
    
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
        iEmpresa                = Empresa.objects.filter(id_empresa=1)[0]
        iIDPasta                = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0].id_pasta
        
        iUpload1                 = MultiuploaderImage()
        iUpload1.key_data        = iUpload1.key_generate
        iUpload1.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload1.fileName       = 'imagem.tif'
        iUpload1.image          = '%s/media_teste/imagem.tif' % settings.MEDIA_ROOT
        iUpload1.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload2                 = MultiuploaderImage()
        iUpload2.key_data        = iUpload2.key_generate
        iUpload2.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload2.fileName       = 'imagem.jpg'
        iUpload2.image          = '%s/media_teste/imagem.jpg' % settings.MEDIA_ROOT
        iUpload2.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload3                 = MultiuploaderImage()
        iUpload3.key_data        = iUpload3.key_generate
        iUpload3.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload3.fileName       = 'imagem.png'
        iUpload3.image          = '%s/media_teste/imagem.png' % settings.MEDIA_ROOT
        iUpload3.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload4                 = MultiuploaderImage()
        iUpload4.key_data        = iUpload4.key_generate
        iUpload4.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload4.fileName       = 'texto.doc'
        iUpload4.image          = '%s/media_teste/texto.doc' % settings.MEDIA_ROOT
        iUpload4.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload5                 = MultiuploaderImage()
        iUpload5.key_data        = iUpload5.key_generate
        iUpload5.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload5.fileName       = 'texto.odt'
        iUpload5.image          = '%s/media_teste/texto.odt' % settings.MEDIA_ROOT
        iUpload5.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload6                 = MultiuploaderImage()
        iUpload6.key_data        = iUpload6.key_generate
        iUpload6.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload6.fileName       = 'texto.txt'
        iUpload6.image          = '%s/media_teste/texto.txt' % settings.MEDIA_ROOT
        iUpload6.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload7                 = MultiuploaderImage()
        iUpload7.key_data        = iUpload7.key_generate
        iUpload7.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload7.fileName       = 'texto.pdf'
        iUpload7.image          = '%s/media_teste/texto.pdf' % settings.MEDIA_ROOT
        iUpload7.save(iIDPasta, iEmpresa.id_empresa)

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
        iDataCriacao    = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iEh_Assinado    = False
        iEh_Versao_Atual= True
        
        iVersao         = 1
        iUpload         = MultiuploaderImage.objects.filter()[0]
        iVersao1        = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao1.save()
        
        iVersao         = 2
        iUpload         = MultiuploaderImage.objects.filter()[1]
        iVersao1        = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao1.save()
        
        iVersao         = 3
        iUpload         = MultiuploaderImage.objects.filter()[2]
        iVersao1        = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao1.save()
        
        iVersao         = 4
        iUpload         = MultiuploaderImage.objects.filter()[3]
        iVersao1        = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao1.save()
        
        iVersao         = 5
        iUpload         = MultiuploaderImage.objects.filter()[4]
        iVersao1        = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao1.save()
        
        iVersao         = 6
        iUpload         = MultiuploaderImage.objects.filter()[5]
        iVersao1        = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao1.save()
        
        iVersao         = 7
        iUpload         = MultiuploaderImage.objects.filter()[6]
        iVersao1        = Versao(documento= iDocumento, usr_criador= iCriador, estado= iEstado, versao= iVersao, 
                                 upload= iUpload, data_criacao= iDataCriacao, eh_assinado= iEh_Assinado, 
                                 eh_versao_atual= iEh_Versao_Atual)
        iVersao1.save()

#libreoffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" --nologo --headless --nofirststartwizard