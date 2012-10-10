
from django.test                                import TestCase
from django.contrib.auth.models                 import User

from models                                     import Empresa
from models                                     import Usuario
from models                                     import Tipo_de_Usuario

import time
import constantes #@UnresolvedImport


class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarTipoUsuario()
        self.mokarUsuario()
        pass

    def tearDown(self):
        time.sleep(2)
        Usuario.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Empresa.objects.all().delete()
        pass


    def testCriarEmpresa(self):
        iNome           = 'teste_001'
        iPastaRaiz      = '/documentos/teste_001/1'
        iEh_Ativo       = True
        iEmpresa        = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa.save(False)
        self.assertEquals(iEmpresa.id_empresa, (Empresa.objects.filter(nome= iNome)[0].id_empresa))
        
    def testCriarTipoUsuario(self):
        iDescricacao= 'Tipo teste'
        iTipoUsuario= Tipo_de_Usuario()
        iTipoUsuario.descricao= iDescricacao
        iTipoUsuario.save()
        self.assertEqual(2, Tipo_de_Usuario.objects.count())
    
    def testCriarUsuario(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario    = Tipo_de_Usuario.objects.all()[0]
        iEmail          = 'usuario@teste.com.br'
        iUsuario        = Usuario(empresa= iEmpresa, email= iEmail, tipo_usuario= iTipoUsuario)
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
        
    def testobtemListaEnderecoEmpresas(self):
        iEmpresas= Empresa.objects.filter()
        iLista= ''
        for i in range(len(iEmpresas)):
            if (iEmpresas[i].rua != '' or iEmpresas[i].bairro != '') and (iEmpresas[i].rua != None or iEmpresas[i].bairro != None):
                iInfo= "%s %s" % (iEmpresas[i].rua, iEmpresas[i].bairro)
                if iLista== '':
                    iLista= str(iEmpresas[i].id_empresa) + '%' + iInfo + '%' + str(iEmpresas[i].nome)
                else:
                    iLista= iLista + '%' + str(iEmpresas[i].id_empresa) + '%' + iInfo + '%' + str(iEmpresas[i].nome)
        self.assertEquals('', iLista)
        
    def testobtemUsuariosComEmailDaEmpresa(self):
        iEmpresa= Empresa.objects.all()[0]
        iListaUsuarios= Usuario.objects.filter(empresa= iEmpresa).filter(
                            tipo_usuario__id_tipo_de_usuario= constantes.cntTipoUsuarioSistema).filter(email__isnull=False)
        self.assertEquals(2, len(iListaUsuarios))
        
    def testobtemContatosComEmailDaEmpresa(self):
        iEmpresa= Empresa.objects.all()[0]
        iListaUsuarios= Usuario.objects.filter(empresa= iEmpresa).filter(
                            tipo_usuario__id_tipo_de_usuario= constantes.cntTipoUsuarioContato).filter(email__isnull=False)
        self.assertEquals(0, len(iListaUsuarios))
    
    def testAutenticaUsuario(self):
        iEmail= 'usuario1@teste.com.br'
        iSenha= '12346'
        iAutenticou= Usuario().autenticaUsuario(iEmail, iSenha)
        self.assertEquals(None, iAutenticou)
        
        iEmail= 'usuario1@teste.com.br'
        iSenha= '12345'
        iAutenticou= Usuario().autenticaUsuario(iEmail, iSenha)
        self.assertEquals(iEmail, iAutenticou.email)
        
        iEmail= 'usuario5@teste.com.br'
        iSenha= '12345'
        iAutenticou= Usuario().autenticaUsuario(iEmail, iSenha)
        self.assertEquals(None, iAutenticou)
        
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
        iTipoUsuario_1  = Tipo_de_Usuario.objects.all()[0]
        iEmail_1        = 'usuario1@teste.com.br'
        iSenha          = '12345'
        iUsuario_1      = Usuario(empresa= iEmpresa_1, email= iEmail_1, tipo_usuario= iTipoUsuario_1, 
                                  password= iSenha)
        iUsuario_1.save()
        
        iEmail_2        = 'usuario2@teste.com.br'
        iUsuario_2      = Usuario(empresa= iEmpresa_1, email= iEmail_2, tipo_usuario= iTipoUsuario_1)
        iUsuario_2.save()
        
        iEmpresa_2      = Empresa.objects.filter(id_empresa= 2)[0]
        iEmail_3        = 'usuario3@teste.com.br'
        iUsuario_3      = Usuario(empresa= iEmpresa_2, email= iEmail_3, tipo_usuario= iTipoUsuario_1)
        iUsuario_3.save()
        
        iEmail_4        = 'usuario4@teste.com.br'
        iUsuario_4      = Usuario(empresa= iEmpresa_2, email= iEmail_4, tipo_usuario= iTipoUsuario_1)
        iUsuario_4.save()