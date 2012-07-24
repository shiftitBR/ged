
from django.test                                import TestCase

from autenticacao.models        import Empresa #@UnresolvedImport
from documento.models           import Versao   #@UnresolvedImport

from models                     import Tipo_de_Indice
from models                     import Indice
from models                     import Indice_Versao_Valor


class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
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
    
    
#    def testCriarIndiceVersaoValor(self):
#        iEmpresa        = Empresa.objects.filter()[0]
#        iIndice         = Indice.objects.filter(empresa= iEmpresa.id_empresa)[0]
#        Versao          = 
    
    #-----------------------------------------------------MOKS---------------------------------------------------
    
    
    def mokarTipoIndice(self):
        iDescricao      = 'inteiro'
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]     
        iTipoIndice     = Tipo_de_Indice(descricao= iDescricao, empresa= iEmpresa)
        iTipoIndice.save()   
        
        
    def mokarEmpresa(self):
        iNome           = 'empresa_001'
        iBanco          = 'shift_ged'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa_1      = Empresa(nome= iNome, banco= iBanco, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_1.save()
        
    def mokarIndice(self):
        iDescricao      = 'valor'
        iTipo           = Tipo_de_Indice.objects.filter(empresa= 1)[0]
        iEmpresa        = Empresa.objects.filter()[0]
        iIndice         = Indice(descricao= iDescricao, tipo_indice= iTipo, empresa= iEmpresa)
        iIndice.save()
        
        