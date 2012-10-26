# -*- coding: utf-8 -*-
'''
Created on Oct 5, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.test                                import TestCase
from PyProject_GED.servidor.models import Servidor, Importacao_FTP,\
    Cadastro_Biometria
from PyProject_GED.autenticacao.models import Empresa, Tipo_de_Usuario, Usuario
from django.contrib.auth.models import User


class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarTipoUsuario()
        self.mokarUsuario()
        self.mokarCriacaoCadastroBiometria()
        pass
    
    
    def tearDown(self):
        Usuario.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Empresa.objects.all().delete()
        pass
    
    def testCriaImportacaoFTP(self):
        iUser= User.objects.all()[0]
        iIPOrigem= '192.168.0.1'
        iImportacao= Importacao_FTP().criaImportacao_FTP(iUser, iIPOrigem)
        self.assertEquals(1, Importacao_FTP.objects.all().count())
        self.assertEquals('1', iImportacao.pasta_temporaria)
    
    def testCriaCadastroBiometria(self):
        iUser= User.objects.all()[0]
        iIPOrigem= '192.168.0.1'
        iCadastro= Cadastro_Biometria().criaCadastroDeBiometria(iUser, iIPOrigem)
        self.assertEquals(2, Cadastro_Biometria.objects.all().count())
        self.assertEquals('1', iCadastro.pasta_destino)
    
    def testExcluiCadastroDeBiometria(self):
        iUsuario= Usuario.objects.all()[1]
        self.assertEquals(1, Cadastro_Biometria.objects.count())
        Cadastro_Biometria().excluiCadastroDeBiometria(iUsuario)
        self.assertEquals(0, Cadastro_Biometria.objects.count())
    
    def testCriaRespostaEmJSONParaImportacao(self):
        iPasta= '1'
        iJSON= Servidor().criaRespostaEmJSON(iPasta)
        self.assertEquals('{"pasta": "1", "ip": "ftp.upspace.com.br", "login": "teste@upspace.com.br", "senha": "importar@051011", "tipo": "1"}', iJSON)
    
    def testCriaRespostaEmJSONParaCadastroBiometrico(self):
        iPasta= '1'
        iIDEmpresa= '1'
        iJSON= Servidor().criaRespostaEmJSON(iPasta, iIDEmpresa)
        self.assertEquals('{"tipo": "1", "usuario": "1", "ip": "ftp.upspace.com.br", "senha": "importar@051011", "pasta": "1", "login": "teste@upspace.com.br"}', iJSON)
    
    def testaSocket(self):
        Servidor().iniciaSocket_TCP()
        
        

#-----------------------------------------------------MOKS---------------------------------------------------  
    
    def mokarEmpresa(self):
        iNome           = 'empresa_001'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa_1      = Empresa(nome= iNome, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa_1.save(False)     

    def mokarTipoUsuario(self):
        iDescricacao= 'Tipo teste'
        iTipoUsuario= Tipo_de_Usuario()
        iTipoUsuario.descricao= iDescricacao
        iTipoUsuario.save()
        
    def mokarUsuario(self):
        iEmpresa       = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario   = Tipo_de_Usuario.objects.all()[0]
        
        iEmail          = 'usuario1@teste.com.br'
        iSenha          = '12345'
        iUsuario_1      = Usuario(empresa= iEmpresa, email= iEmail, tipo_usuario= iTipoUsuario, password= iSenha)
        iUsuario_1.save()
                
        iEmail          = 'usuario2@teste.com.br'
        iUsuario_2      = Usuario(empresa= iEmpresa, email= iEmail, tipo_usuario= iTipoUsuario)
        iUsuario_2.save()
    
    def mokarCriacaoCadastroBiometria(self):
        iUser= User.objects.all()[1]
        iIPOrigem= '192.168.0.2'
        iCadastro= Cadastro_Biometria().criaCadastroDeBiometria(iUser, iIPOrigem)