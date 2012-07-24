
from django.test                                import TestCase

from autenticacao.models                        import Empresa #@UnresolvedImport
from autenticacao.models                        import Usuario #@UnresolvedImport
from autenticacao.models                        import Tipo_de_Usuario #@UnresolvedImport
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
        self.mokarTipoUsuario()
        self.mokarUsuario()
        self.mokarPasta()
        self.mokarTipoDocumento()
        self.mokarMultiUploader()
        self.mokarDocumento()
        self.mokarEstadoVersao()
        pass
    
    
    def tearDown(self):
        Empresa.objects.all().delete()
        #Usuario.objects.all().delete()
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
        
    def testCriarEstadoVersao(self):
        iDescricao      = 'Disponivel'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
        self.assertEquals(iEstadoVersao.id_estado_da_versao, Estado_da_Versao.objects.filter(id_estado_da_versao=2)[0].id_estado_da_versao)
    
    def testCriarDocumento(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento  = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iPasta          = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iAssunto        = 'Teste'
        iVersaoAtual    = 1
        iEhPublico      = True
        iDocumento      = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    versao_atual= iVersaoAtual, eh_publico= iEhPublico)
        iDocumento.save()
        self.assertEquals(iDocumento.id_documento, Documento.objects.filter(empresa= iEmpresa.id_empresa).filter(id_documento= 2)[0].id_documento)
    
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
        self.assertEquals(iVersao.id_versao, Versao.objects.filter(id_versao= 1)[0].id_versao)
        
    #-----------------------------------------------------MOKS---------------------------------------------------
    
    
    def mokarEmpresa(self):
        iNome           = 'empresa_001'
        iBanco          = 'shift_ged'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa_1      = Empresa(nome= iNome, banco= iBanco, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_1.save()
        
        iNome           = 'empresa_002'
        iBanco          = 'shift_ged'
        iPastaRaiz      = '/documentos/empresa_002/2'
        iEh_Ativo       = True
        iEmpresa_2      = Empresa(nome= iNome, banco= iBanco, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_2.save()
    
    def mokarTipoUsuario(self):
        iDescricao      = 'administador'
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario_1  = Tipo_de_Usuario(descricao= iDescricao, empresa= iEmpresa)
        iTipoUsuario_1.save()
        
    def mokarUsuario(self):
        iEmpresa_1      = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(empresa= iEmpresa_1.id_empresa).filter(descricao= 'administador')[0]
        iEh_Ativo       = True
        iUsuario_1      = Usuario(empresa= iEmpresa_1, tipo_usuario= iTipoUsuario, eh_ativo= iEh_Ativo)
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
        iUpload.save(iIDPasta)

    def mokarDocumento(self):
        iEmpresa        = Empresa.objects.filter(id_empresa=1)[0]
        iTipoDocumento  = Tipo_de_Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iResponsavel    = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iPasta          = Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iAssunto        = 'Teste'
        iVersaoAtual    = 1
        iEhPublico      = True
        iDocumento      = Documento(empresa= iEmpresa, tipo_documento= iTipoDocumento, 
                                    usr_responsavel= iResponsavel, pasta= iPasta, assunto= iAssunto, 
                                    versao_atual= iVersaoAtual, eh_publico= iEhPublico)
        iDocumento.save()
        
    def mokarEstadoVersao(self):
        iDescricao      = 'Disponivel'
        iEstadoVersao   = Estado_da_Versao(descricao= iDescricao)
        iEstadoVersao.save() 
    
    
    