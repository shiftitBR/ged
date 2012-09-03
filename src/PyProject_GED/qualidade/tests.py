
from django.test                                import TestCase

from models                                     import Tipo_de_Norma, Norma_Documento, Norma 
from PyProject_GED.autenticacao.models          import Tipo_de_Usuario, Usuario,\
    Empresa
from PyProject_GED.seguranca.models             import Grupo_Usuario, Pasta
from PyProject_GED.documento.models             import Tipo_de_Documento, Documento

class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarTipoNorma()
        self.mokarNorma()
        self.mokarTipoUsuario()
        self.mokarUsuario()
        self.mokarPasta()
        self.mokarTipoDocumento()
        self.mokarDocumento()
        self.mokarNormaDocumento()
        pass
    
    
    def tearDown(self):
        Empresa.objects.all().delete()
        Pasta.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Usuario.objects.all().delete()
        Grupo_Usuario.objects.all().delete()
        Tipo_de_Norma.objects.all().delete()
        Norma.objects.all().delete()
        Norma_Documento.objects.all().delete()
        pass
    
    
    def testCriarTipoNorma(self):
        iDescricao       = 'ABNT'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoNorma       = Tipo_de_Norma(descricao= iDescricao, empresa=iEmpresa)
        iTipoNorma.save()
        self.assertEquals(iTipoNorma.id_tipo_norma, 2)
    
    def testCriarNorma(self):
        iEmpresa            = Empresa.objects.filter(id_empresa= 1)[0]
        iNorma= Norma()
        iNorma.tipo_norma   = Tipo_de_Norma.objects.filter(empresa= iEmpresa)[0]
        iNorma.empresa      = iEmpresa
        iNorma.descricao    = 'bla bla bla'
        iNorma.norma_pai    = None
        iNorma.save()
        self.assertEquals(iNorma.id_norma, 2)
        
    def testCriarNormaDocumento(self):
        iNorma           = Norma.objects.filter(empresa= 1)[0]
        iDocumento       = Documento.objects.filter(empresa= 1)[0]
        iNormaDocumento  = Norma_Documento(norma= iNorma, documento= iDocumento)
        iNormaDocumento.save()
        self.assertEquals(iNormaDocumento.id_norma_documento, 2)
    
    def testObtemNorma(self):
        iNorma           = Norma.objects.filter(empresa= 1)[0]
        self.assertEquals(iNorma.id_norma, 1)
    
    def testObtemDocumentosPelaNorma(self):
        iNorma= Norma.objects.filter(empresa= 1)[0]
        iListaDocumentos= Norma_Documento().obtemDocumentosPelaNorma(iNorma)
        self.assertEquals(1, len(iListaDocumentos))
    
    #-----------------------------------------------------MOKS---------------------------------------------------  
    
    def mokarEmpresa(self):
        iNome           = 'empresa_001'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa_1      = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_1.save(False)
    
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
        iNorma.descricao    = 'bla bla bla'
        iNorma.norma_pai    = None
        iNorma.save()
        
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
    
    def mokarNormaDocumento(self):
        iNorma           = Norma.objects.filter(empresa= 1)[0]
        iDocumento       = Documento.objects.filter(empresa= 1)[0]
        iNormaDocumento  = Norma_Documento(norma= iNorma, documento= iDocumento)
        iNormaDocumento.save()