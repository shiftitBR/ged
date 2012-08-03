
from django.test                                import TestCase
from django.contrib.auth.models                 import User

from models                                     import Empresa
from models                                     import Usuario
from PyProject_GED.seguranca.models             import Pasta

import time

class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarUsuario()
        pass

    def tearDown(self):
        time.sleep(2)
        Pasta.objects.all().delete()
        Empresa.objects.all().delete()
        Usuario.objects.all().delete()
        pass


    def testCriarEmpresa(self):
        iNome           = 'teste_001'
        iPastaRaiz      = '/documentos/teste_001/1'
        iEh_Ativo       = True
        iEmpresa        = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa.save(False)
        self.assertEquals(iEmpresa.id_empresa, (Empresa.objects.filter(nome= iNome)[0].id_empresa))
        
    def testCriarUsuario(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iEmail          = 'usuario@teste.com.br'
        iUsuario        = Usuario(empresa= iEmpresa, email= iEmail)
        iUsuario.save()
        self.assertEquals(iUsuario.id, (Usuario.objects.filter(email= 'usuario@teste.com.br')[0].id))
    
    def testObtemUsuario(self):
        iUsuario= Usuario.objects.all()[0]
        iUser= User.objects.filter(pk= iUsuario.pk)[0]
        iUsuario2= Usuario().obtemUsuario(iUser)
        self.assertEquals(iUsuario.email, iUsuario2.email)
    
    def testObtemUsuarioPeloID(self):
        iIDUsuario= Usuario.objects.all()[0].id
        iUsuario= Usuario().obtemUsuarioPeloID(iIDUsuario)
        self.assertEquals(iIDUsuario, iUsuario.id)
    
    def testObtemEmpresaDoUsuario(self):
        iUsuario= Usuario.objects.all()[0]
        iEmpresa= Usuario().obtemEmpresaDoUsuario(iUsuario.id)
        self.assertEquals(iUsuario.empresa, iEmpresa)
    
    def testObtemUsuariosDaEmpresa(self):
        iEmpresa= Empresa.objects.all()[0]
        iListaUsuarios= Usuario().obtemUsuariosDaEmpresa(iEmpresa)
        self.assertEquals(2, len(iListaUsuarios))
        
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
        iEmail_1        = 'usuario1@teste.com.br'
        iUsuario_1      = Usuario(empresa= iEmpresa_1, email= iEmail_1)
        iUsuario_1.save()
        
        iEmail_2        = 'usuario2@teste.com.br'
        iUsuario_2      = Usuario(empresa= iEmpresa_1, email= iEmail_2)
        iUsuario_2.save()
        
        iEmpresa_2      = Empresa.objects.filter(id_empresa= 2)[0]
        iEmail_3        = 'usuario3@teste.com.br'
        iUsuario_3      = Usuario(empresa= iEmpresa_2, email= iEmail_3)
        iUsuario_3.save()
        
        iEmail_4        = 'usuario4@teste.com.br'
        iUsuario_4      = Usuario(empresa= iEmpresa_2, email= iEmail_4)
        iUsuario_4.save()