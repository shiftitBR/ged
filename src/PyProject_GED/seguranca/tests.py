
from django.test                                import TestCase

from autenticacao.models                        import Empresa #@UnresolvedImport

from models                                     import Pasta 
from models                                     import Grupo
from models                                     import Funcao
from models                                     import Firewall
from models                                     import Grupo_Pasta
from models                                     import Funcao_Grupo
from models                                     import Firewall_Grupo        

class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarGrupo()
        self.mokarPasta()
        self.mokarFuncao()
        self.mokarFirewall()
        pass
    
    
    def tearDown(self):
        Empresa.objects.all().delete()
        pass
    
    def testCriarPasta(self):
        iNome            = 'Modelo'
        iDiretorio       = '/'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iPasta           = Pasta(nome= iNome, diretorio= iDiretorio, empresa= iEmpresa)
        iPasta.save()
        self.assertEquals(iPasta.id_pasta, Pasta.objects.filter(id_pasta= 2)[0].id_pasta)
    
    def testCriaPasta(self):
        iEmpresa= Empresa.objects.all()[0]
        iNomePastaFilha= 'Teste Filha'
        iNomePastaRaiz= 'Teste Raiz'
        iPastaPai= Pasta.objects.all()[0]
        iPastaRaiz= Pasta().criaPasta(iEmpresa, iNomePastaRaiz)
        iPastaFilha= Pasta().criaPasta(iEmpresa, iNomePastaFilha, iPastaPai)
        self.assertEquals(iNomePastaFilha, iPastaFilha.nome)
        self.assertEquals(iNomePastaRaiz, iPastaRaiz.nome)
    
#    def testObtemDiretorioUpload(self):
#        iIDPasta= Pasta.objects.all()[0].id_pasta
#        iIDEmpresa= Empresa.objects.all()[0].id_empresa
#        iDiretorio= Pasta().obtemDiretorioUpload(iIDPasta, iIDEmpresa)
#        self.assertEquals('/home/spengler/Git/GED/PyProject_GED/src/PyProject_GED/media/documentos/empresa_001/1', iDiretorio)

    def testMontaDiretorioPasta(self):
        iPasta= Pasta.objects.all()[0]
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        iDiretorio= Pasta().montaDiretorioPasta(iIDEmpresa, iPasta)
        self.assertEquals('/home/spengler/Git/GED/PyProject_GED/src/PyProject_GED/media/documentos/empresa_001/1', iDiretorio)
    
    def testObtemNomePasta(self):
        iIDPasta= Pasta.objects.all()[0].id_pasta
        iNome= Pasta().obtemNomeDaPasta(iIDPasta)
        self.assertEquals('Modelo', iNome)
    
    def testCriarGrupoPasta(self):
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iPasta           = Pasta.objects.filter(empresa= 1)[0]
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupoPasta      = Grupo_Pasta(grupo= iGrupo, pasta= iPasta, empresa= iEmpresa)
        iGrupoPasta.save()
        self.assertEquals(iGrupoPasta.id_grupo_pasta, Grupo_Pasta.objects.filter(empresa= iEmpresa.id_empresa)[0].id_grupo_pasta)

    def testCriarFuncaoGrupo(self):
        iFuncao          = Funcao.objects.filter(empresa= 1)[0]
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iFuncaoGrupo     = Funcao_Grupo(funcao= iFuncao, grupo= iGrupo)
        iFuncaoGrupo.save()
        self.assertEquals(iFuncaoGrupo.id_funcao_grupo, Funcao_Grupo.objects.filter(funcao= iFuncao.id_funcao)[0].id_funcao_grupo)
        
    def testCriarFirewallGrupo(self):
        iFirewall        = Firewall.objects.filter(empresa= 1)[0]
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iFirewallGrupo   = Firewall_Grupo(firewall= iFirewall, grupo= iGrupo)
        iFirewallGrupo.save()
        self.assertEquals(iFirewallGrupo.id_firewall_grupo, Firewall_Grupo.objects.filter(firewall= iFirewall.id_firewall)[0].id_firewall_grupo)
            
    #-----------------------------------------------------MOKS---------------------------------------------------  
    
    def mokarEmpresa(self):
        iNome           = 'empresa_001'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa_1      = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_1.save(False)
    
    def mokarPasta(self):
        iNome            = 'Modelo'
        iDiretorio       = '/'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iPasta           = Pasta(nome= iNome, diretorio= iDiretorio, empresa= iEmpresa)
        iPasta.save()
        
    def mokarGrupo(self):
        iNome            = 'Teste'
        iDescricao       = 'Colaboradores'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupo           = Grupo(nome= iNome, descricao= iDescricao, empresa= iEmpresa)
        iGrupo.save()
    
    def mokarFuncao(self):
        iNome            = 'teste'
        iDescricao       = 'teste'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iFuncao          = Funcao(nome= iNome, descricao= iDescricao, empresa= iEmpresa)
        iFuncao.save()
        
    def mokarFirewall(self):
        iIp              = '1939393939'
        iDescricao       = 'teste'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iFirewal         = Firewall(ip= iIp, descricao= iDescricao, empresa= iEmpresa)
        iFirewal.save()