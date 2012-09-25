
from django.test                                import TestCase
from django.conf                                import settings

from models                                     import Pasta 
from models                                     import Grupo
from models                                     import Funcao
from models                                     import Firewall
from models                                     import Grupo_Pasta
from models                                     import Funcao_Grupo
from models                                     import Firewall_Grupo  
      
from PyProject_GED.autenticacao.models          import Tipo_de_Usuario, Usuario,\
    Empresa
from PyProject_GED.seguranca.models             import Grupo_Usuario

class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarGrupo()
        self.mokarPasta()
        self.mokarFuncao()
        self.mokarFirewall()
        self.mokarGrupoPasta()
        self.mokarFuncaoGrupo()
        self.mokarFirewallGrupo()
        self.mokarTipoUsuario()
        self.mokarUsuario()
        self.mokarGrupo_Usuario()
        pass
    
    
    def tearDown(self):
        Empresa.objects.all().delete()
        Pasta.objects.all().delete()
        Grupo.objects.all().delete()
        Funcao.objects.all().delete()
        Firewall.objects.all().delete()
        Grupo_Pasta.objects.all().delete()
        Funcao_Grupo.objects.all().delete()
        Firewall_Grupo.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Usuario.objects.all().delete()
        Grupo_Usuario.objects.all().delete()
        pass
        
    def testCriarPasta(self):
        iNome            = 'Modelo'
        iDiretorio       = '/'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iPasta           = Pasta(nome= iNome, diretorio= iDiretorio, empresa= iEmpresa)
        iPasta.save(False)
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
    
    def testObtemDiretorioUpload(self):
        iIDPasta= Pasta.objects.all()[0].id_pasta
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        iDiretorio= Pasta().obtemDiretorioUpload(iIDPasta, iIDEmpresa)
        self.assertEquals(settings.PROJECT_ROOT_PATH + '/media/documentos/empresa_001/1', iDiretorio)

    def testMontaDiretorioPasta(self):
        iPasta= Pasta.objects.all()[0]
        iIDEmpresa= Empresa.objects.all()[0].id_empresa
        iDiretorio= Pasta().montaDiretorioPasta(iIDEmpresa, iPasta)
        self.assertEquals('1', iDiretorio)
    
    def testObtemNomePasta(self):
        iIDPasta= Pasta.objects.all()[0].id_pasta
        iNome= Pasta().obtemNomeDaPasta(iIDPasta)
        self.assertEquals('Modelo', iNome)
    
    def testCriarGrupoPasta(self):
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iPasta           = Pasta.objects.filter(empresa= 1)[0]
        iGrupoPasta      = Grupo_Pasta(grupo= iGrupo, pasta= iPasta)
        iGrupoPasta.save()
        self.assertEquals(iGrupoPasta.id_grupo_pasta, Grupo_Pasta.objects.all()[1].id_grupo_pasta)

    def testCriarFuncaoGrupo(self):
        iFuncao          = Funcao.objects.filter()[0]
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
            
    def testverificaIP(self):
        iEmpresa    = Empresa.objects.filter(id_empresa= 1)[0]
        iIP         = '127.0.0.1'
        iPossivel= False
        iListaFirewall= Firewall.objects.filter(empresa= iEmpresa)
        if len(iListaFirewall) == 0:
            return True
        iListaIP= iIP.split('.')
        for i in range(len(iListaFirewall)):
            iFirewall= iListaFirewall[i].ip.split('.')
            if iListaIP[0] == iFirewall[0] and iListaIP[1] == iFirewall[1] and iListaIP[2] == iFirewall[2] and iListaIP[3] == iFirewall[3]:
                iPossivel=True
            elif iFirewall[2] == '0' and iFirewall[3] == '0':
                if iListaIP[0] == iFirewall[0] and iListaIP[1] == iFirewall[1]:
                    iPossivel=True
        self.assertEquals(iPossivel , True)      
    
    def testobtemListaGrupoPasta(self):
        iGrupo = Grupo.objects.filter(empresa= 1)[0]
        iLista = Grupo_Pasta.objects.filter(grupo= iGrupo)[0]
        self.assertEquals(1 , iLista.id_grupo_pasta) 
        
    def testpossuiAcessoPasta(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iUsuario        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iGrupoUsuario   = Grupo_Usuario().obtemGrupoUsuario(iUsuario)
        iLista          = Grupo_Pasta.objects.filter(grupo= iGrupoUsuario.grupo.id_grupo)
        iPossuiAcesso   = False
        for i in range(len(iLista)):
            if int(1) == int(iLista[i].pasta.id_pasta):
                iPossuiAcesso= True
        self.assertEquals(iPossuiAcesso , True)
        
    def testcriaGrupo_Usuario(self):
        iEmpresa              = Empresa.objects.filter(id_empresa= 1)[0]
        iUsuario              = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iGrupo                = Grupo.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iGrupo_Usuario        = Grupo_Usuario()
        iGrupo_Usuario.grupo  = iGrupo
        iGrupo_Usuario.usuario= iUsuario
        iGrupo_Usuario.save()
        self.assertEquals(2 , iGrupo_Usuario.id_grupo_usuario)
        
    def testobtemGrupoUsuario(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iUsuario        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iGrupoUsuario   = Grupo_Usuario.objects.filter(usuario= iUsuario.id)[0]
        self.assertEquals(1 , iGrupoUsuario.id_grupo_usuario)
        
    def testobtemListaFuncaoGrupo(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupo          = Grupo.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iListaFuncoes   = Funcao_Grupo.objects.filter(grupo= iGrupo)
        self.assertEquals(2 , len(iListaFuncoes))
        
    def testpossuiAcessoFuncao(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iUsuario        = Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iGrupoUsuario   = Grupo_Usuario().obtemGrupoUsuario(iUsuario)
        iLista          = Funcao_Grupo.objects.filter(grupo= iGrupoUsuario.grupo.id_grupo)
        iPossuiAcesso   = False
        for i in range(len(iLista)):
            if int(1) == int(iLista[i].funcao.id_funcao):
                iPossuiAcesso= True
        self.assertEquals(iPossuiAcesso , True)
        
    def testExcluiFuncoesDoGrupo(self):
        iGrupo          = Grupo.objects.all()[1]
        iListaFuncoes   = Funcao_Grupo.objects.filter(grupo= iGrupo.id_grupo)
        self.assertEquals(2, len(iListaFuncoes))
        Funcao_Grupo().excluiFuncoesDoGrupo(iGrupo)
        iListaFuncoes   = Funcao_Grupo.objects.filter(grupo= iGrupo.id_grupo)
        self.assertEquals(0,  len(iListaFuncoes))
    
    def testObtemListaDeGruposSemFuncao(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iLista= Funcao_Grupo().obtemListaDeGruposSemFuncao(iEmpresa)
        self.assertEquals(1, len(iLista))
    
    def testExcluiUsuariosDoGrupo(self):
        iGrupo          = Grupo.objects.all()[1]
        iListaUsuarios  = Grupo_Usuario.objects.filter(grupo= iGrupo.id_grupo)
        self.assertEquals(1, len(iListaUsuarios))
        Grupo_Usuario().excluiUsuariosDoGrupo(iGrupo)
        iListaUsuarios   = Grupo_Usuario.objects.filter(grupo= iGrupo.id_grupo)
        self.assertEquals(0,  len(iListaUsuarios))
    
    def testObtemListaDeGruposSemUsuario(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iLista= Grupo_Usuario().obtemListaDeGruposSemUsuario(iEmpresa)
        self.assertEquals(1, len(iLista))
    
    def testExcluiPastasDoGrupo(self):
        iGrupo          = Grupo.objects.all()[1]
        iListaPastas    = Grupo_Pasta.objects.filter(grupo= iGrupo.id_grupo)
        self.assertEquals(1, len(iListaPastas))
        Grupo_Pasta().excluiPastasDoGrupo(iGrupo)
        iListaPastas   = Grupo_Pasta.objects.filter(grupo= iGrupo.id_grupo)
        self.assertEquals(0,  len(iListaPastas))
    
    def testObtemListaDeGruposSemPasta(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iLista= Grupo_Pasta().obtemListaDeGruposSemPasta(iEmpresa)
        self.assertEquals(1, len(iLista))
    
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
        iPasta.save(False)
        
    def mokarGrupo(self):
        iNome            = 'Teste'
        iDescricao       = 'Colaboradores'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupo           = Grupo(nome= iNome, descricao= iDescricao, empresa= iEmpresa)
        iGrupo.save()
        
        iNome            = 'Teste2'
        iDescricao       = 'Colaboradores2'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupo           = Grupo(nome= iNome, descricao= iDescricao, empresa= iEmpresa)
        iGrupo.save()
        
    def mokarGrupoPasta(self):
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iPasta           = Pasta.objects.filter(empresa= 1)[0]
        iGrupoPasta      = Grupo_Pasta(grupo= iGrupo, pasta= iPasta)
        iGrupoPasta.save()
    
    def mokarFuncao(self):
        iNome            = 'teste'
        iDescricao       = 'teste'
        iFuncao          = Funcao(nome= iNome, descricao= iDescricao)
        iFuncao.save()
        
        iNome            = 'teste2'
        iDescricao       = 'teste2'
        iFuncao          = Funcao(nome= iNome, descricao= iDescricao)
        iFuncao.save()
        
    def mokarFuncaoGrupo(self):
        iFuncao          = Funcao.objects.filter()[0]
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iFuncaoGrupo     = Funcao_Grupo(funcao= iFuncao, grupo= iGrupo)
        iFuncaoGrupo.save()
        
        iFuncao          = Funcao.objects.filter()[1]
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iFuncaoGrupo     = Funcao_Grupo(funcao= iFuncao, grupo= iGrupo)
        iFuncaoGrupo.save()
        
    def mokarFirewall(self):
        iIp              = '127.0.0.1'
        iDescricao       = 'teste'
        iEmpresa         = Empresa.objects.filter(id_empresa= 1)[0]
        iFirewal         = Firewall(ip= iIp, descricao= iDescricao, empresa= iEmpresa)
        iFirewal.save()
        
    def mokarFirewallGrupo(self):
        iFirewall        = Firewall.objects.filter(empresa= 1)[0]
        iGrupo           = Grupo.objects.filter(empresa= 1)[0]
        iFirewallGrupo   = Firewall_Grupo(firewall= iFirewall, grupo= iGrupo)
        iFirewallGrupo.save()
        
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
        
    def mokarGrupo_Usuario(self):
        iEmpresa              = Empresa.objects.filter(id_empresa= 1)[0]
        iGrupo_Usuario        = Grupo_Usuario()
        iGrupo_Usuario.grupo  = Grupo.objects.filter(empresa= 1)[0]
        iGrupo_Usuario.usuario= Usuario.objects.filter(empresa= iEmpresa)[0]
        iGrupo_Usuario.save()