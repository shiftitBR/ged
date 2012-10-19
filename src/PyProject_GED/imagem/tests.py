'''
Created on Sep 13, 2012

@author: spengler
'''

from django.test                            import TestCase
from controle                               import Controle as ControleImagem
from django.conf                            import settings
from PyProject_GED.autenticacao.models      import Empresa, Usuario,\
    Tipo_de_Usuario
from PyProject_GED.seguranca.models         import Pasta
from PyProject_GED.documento.models         import Tipo_de_Documento, Documento, Estado_da_Versao, Versao
from PyProject_GED.multiuploader.models     import MultiuploaderImage

import datetime
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
        pass
    
    def testCoverteImagemJPGparaPNG(self):
        iVersao= Versao.objects.filter(id_versao= 2)[0]
        iConversao= ControleImagem().converteExtencaoImagem(iVersao.id_versao, constantes.cntExtencaoImagemPNG)
        self.assertEquals(True, len(iConversao) > 0)
    
    def testCoverteImagemJPGparaBMP(self):
        iVersao= Versao.objects.filter(id_versao= 2)[0]
        iConversao= ControleImagem().converteExtencaoImagem(iVersao.id_versao, constantes.cntExtencaoImagemBMP)
        self.assertEquals(True, len(iConversao) > 0)
    
    def testCoverteImagemJPGparaTIF(self):
        iVersao= Versao.objects.filter(id_versao= 2)[0]
        iConversao= ControleImagem().converteExtencaoImagem(iVersao.id_versao, constantes.cntExtencaoImagemTIF)
        self.assertEquals(True, len(iConversao) > 0)
    
    def testCoverteImagemPNGparaJPG(self):
        iVersao= Versao.objects.filter(id_versao= 3)[0]
        iConversao= ControleImagem().converteExtencaoImagem(iVersao.id_versao, constantes.cntExtencaoImagemJPG)
        self.assertEquals(True, len(iConversao) > 0)

    def testEhExportaval(self):
        iVersaoExportavel= Versao.objects.filter(id_versao= 3)[0]
        iVersaoNaoExportavel= Versao.objects.filter(id_versao= 5)[0]
        iEhExportaval= ControleImagem().verificaSeImagemEhExportavel(iVersaoExportavel)
        self.assertEquals(True, iEhExportaval)
        iEhExportaval= ControleImagem().verificaSeImagemEhExportavel(iVersaoNaoExportavel)
        self.assertEquals(False, iEhExportaval)
        
    def testDeletaImagemTemporaria(self):
        iVersao= Versao.objects.filter(id_versao= 3)[0]
        iDiretorio= ControleImagem().converteExtencaoImagem(iVersao.id_versao, constantes.cntExtencaoImagemJPG)
        iDeleta= ControleImagem().deletaImagemTemporaria(iDiretorio)
        self.assertEquals(True, iDeleta)

    def testComprimeJPG(self):
        iVersao= Versao.objects.filter(id_versao= 2)[0]
        iComprimiu= ControleImagem().comprimeImagem(iVersao)
        self.assertEquals(True, iComprimiu)
        
    def testObtemDiretorioDaImagemTemporaria(self):    
        iVersao= Versao.objects.filter(id_versao= 2)[0]
        iDiretorio= ControleImagem().obtemDiretorioDaImagemTemporaria(iVersao.id_versao)
        self.assertEquals('%s/media_teste/temp/imagem_jpg.jpg' % settings.MEDIA_ROOT, iDiretorio)
    
    def testCriaImagemTemporaria(self):    
        iVersao= Versao.objects.filter(id_versao= 2)[0]
        iIDUsuario= 1
        iDiretorio= ControleImagem().criaImagemTemporaria(iVersao, iIDUsuario)
        self.assertEquals('%s/media_teste/temp/1/imagem_jpg.jpg' % settings.MEDIA_ROOT, iDiretorio)
        
    def testInverteImagem(self):
        iDiretorioImagem= '%s/media_teste/temp/1/imagem_jpg.jpg' % settings.MEDIA_ROOT
        iNegativou= ControleImagem().negativaImagem(iDiretorioImagem)
        self.assertEquals(True, iNegativou)
    
    def testRotacionaDocumento(self):
        iDiretorioImagem= '%s/media_teste/temp/1/imagem_jpg.jpg' % settings.MEDIA_ROOT
        iRotacao= -230
        iRotacionou= ControleImagem().rotacionaImagem(iDiretorioImagem, iRotacao)
        self.assertEquals(True, iRotacionou)
        
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
        iPasta.save(False)
        
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
        iUpload1.fileName       = 'imagem_tif.tif'
        iUpload1.image          = '%s/media_teste/imagem_tif.tif' % settings.MEDIA_ROOT
        iUpload1.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload2                 = MultiuploaderImage()
        iUpload2.key_data        = iUpload2.key_generate
        iUpload2.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload2.fileName       = 'imagem_jpg.jpg'
        iUpload2.image          = '%s/media_teste/imagem_jpg.jpg' % settings.MEDIA_ROOT
        iUpload2.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload3                 = MultiuploaderImage()
        iUpload3.key_data        = iUpload3.key_generate
        iUpload3.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload3.fileName       = 'imagem_png.png'
        iUpload3.image          = '%s/media_teste/imagem_png.png' % settings.MEDIA_ROOT
        iUpload3.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload4                 = MultiuploaderImage()
        iUpload4.key_data        = iUpload4.key_generate
        iUpload4.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload4.fileName       = 'imagem_bmp.bmp'
        iUpload4.image          = '%s/media_teste/imagem_bmp.bmp' % settings.MEDIA_ROOT
        iUpload4.save(iIDPasta, iEmpresa.id_empresa)
        
        iUpload5                 = MultiuploaderImage()
        iUpload5.key_data        = iUpload5.key_generate
        iUpload5.upload_date     = datetime.datetime(2012, 02, 15, 15, 10, 45)
        iUpload5.fileName       = 'texto.odt'
        iUpload5.image          = '%s/media_teste/texto.odt' % settings.MEDIA_ROOT
        iUpload5.save(iIDPasta, iEmpresa.id_empresa)

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