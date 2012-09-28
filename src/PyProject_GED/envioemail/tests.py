# -*- coding: utf-8 -*-
from django.test                                import TestCase

from django.core                                import mail

from PyProject_GED.autenticacao.models          import Empresa, Tipo_de_Usuario, Usuario
from PyProject_GED.envioemail.models            import Publicacao,\
    Publicacao_Usuario, Publicacao_Documento, Tipo_de_Email, Email
from PyProject_GED.documento.models             import Tipo_de_Documento,\
    Documento
from PyProject_GED.seguranca.models             import Pasta
from PyProject_GED                              import constantes
from controle                                   import Controle as EnvioEmailControle

class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarTipoUsuario()
        self.mokarUsuario()
        self.mokarPublicacao()
        self.mokarPublicacaoUsuario()
        self.mokarPasta()
        self.mokarTipoDocumento()
        self.mokarDocumento()
        self.mokarPublicacaoDocumento()
        self.mokarTipoDeEmail()
        self.mokarEmail()
        pass
    
    
    def tearDown(self):
        Empresa.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Usuario.objects.all().delete()
        Publicacao.objects.all().delete()
        Publicacao_Usuario.objects.all().delete()
        Tipo_de_Documento.objects.all().delete()
        Documento.objects.all().delete()
        Pasta.objects.all().delete()
        pass
    
    def testcriarPublicacao(self):
        iUsuario                    = Usuario.objects.all()[0]
        iPublicacao                 = Publicacao()
        iPublicacao.usr_remetente   = iUsuario
        iPublicacao.save()
        self.assertEquals(2, iPublicacao.id_publicacao)
        
    def testobtemPublicacao(self):
        iPublicacao = Publicacao.objects.all()[0]
        self.assertEquals(1, iPublicacao.id_publicacao)
        
    def testcriarPublicacaoUsuario(self):
        iPublicacao                     = Publicacao.objects.all()[0]
        iUsuario                        = Usuario.objects.all()[0]
        iPublicacaoUsr                  = Publicacao_Usuario()
        iPublicacaoUsr.publicacao       = iPublicacao
        iPublicacaoUsr.usr_destinatario = iUsuario
        iPublicacaoUsr.save()
        self.assertEquals(2, iPublicacaoUsr.id_publicacao_usuario)
        
    def testobtemListaPublicacaoUsuario(self):
        iPublicacao             = Publicacao.objects.all()[0]
        iListaPublicacaoUsuario = Publicacao_Usuario.objects.filter(publicacao= iPublicacao)
        self.assertEquals(1, iListaPublicacaoUsuario[0].id_publicacao_usuario)
        
    def testcriarPublicacaoDocumento(self):
        iPublicacao                     = Publicacao.objects.all()[0]
        iEmpresa                        = Empresa.objects.filter(id_empresa=1)[0]
        iDocumento                      = Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iPublicacaoDoc                  = Publicacao_Documento()
        iPublicacaoDoc.publicacao       = iPublicacao
        iPublicacaoDoc.documento        = iDocumento
        iPublicacaoDoc.save()
        self.assertEquals(2, iPublicacaoDoc.id_publicacao_documento)
        
    def testobtemListaPublicacaoDocumento(self):
        iPublicacao                 = Publicacao.objects.all()[0]
        iListaPublicacaoDocumento   = Publicacao_Documento.objects.filter(publicacao= iPublicacao)
        self.assertEquals(1, iListaPublicacaoDocumento[0].id_publicacao_documento)
        
    def testEnviandoEmail(self):
        iTitulo = 'Mensagem enviada pelo site'
        iDestino = 'alexandre.spengler@shiftit.com.br'
        iRemetente= 'diego.costa@shiftit.com.br'
        iTexto = """
        Email enviado!
        """
        EnvioEmailControle().enviarEmail(iTitulo, iTexto, iDestino, iRemetente)    
        
        self.assertEquals(mail.outbox[0].subject, 'Mensagem enviada pelo site')

        
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
        iEmpresa       = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario   = Tipo_de_Usuario.objects.all()[0]
        
        iEmail          = 'usuario1@teste.com.br'
        iUsuario_1      = Usuario(empresa= iEmpresa, email= iEmail, tipo_usuario= iTipoUsuario)
        iUsuario_1.save()
        
        iEmail          = 'usuario2@teste.com.br'
        iUsuario_2      = Usuario(empresa= iEmpresa, email= iEmail, tipo_usuario= iTipoUsuario)
        iUsuario_2.save()
        
    def mokarPublicacao(self):
        iUsuario                    = Usuario.objects.all()[0]
        iPublicacao                 = Publicacao()
        iPublicacao.usr_remetente   = iUsuario
        iPublicacao.save()
        
    def mokarPublicacaoUsuario(self):
        iPublicacao                     = Publicacao.objects.all()[0]
        iUsuario                        = Usuario.objects.all()[0]
        iPublicacaoUsr                  = Publicacao_Usuario()
        iPublicacaoUsr.publicacao       = iPublicacao
        iPublicacaoUsr.usr_destinatario = iUsuario
        iPublicacaoUsr.save()
        
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
        
    def mokarPublicacaoDocumento(self):
        iPublicacao                     = Publicacao.objects.all()[0]
        iEmpresa                        = Empresa.objects.filter(id_empresa=1)[0]
        iDocumento                      = Documento.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iPublicacaoDoc                  = Publicacao_Documento()
        iPublicacaoDoc.publicacao       = iPublicacao
        iPublicacaoDoc.documento        = iDocumento
        iPublicacaoDoc.save()


    def mokarTipoDeEmail(self):
        iIDTipo= 1
        iDescricao= 'Pendencia Recebida'
        
        iTipoEmail1= Tipo_de_Email(id_tipo_email= iIDTipo, descricao= iDescricao)
        iTipoEmail1.save()
    
    def mokarEmail(self):
        iIDEmail= 1
        iTipoEmail= Tipo_de_Email.objects.filter(id_tipo_email= constantes.cntTipoEmailPendenciaRecebida)[0]
        iTitulo= """Pendencia Recebida"""
        iMensagem= """
                    Bla bla bla
                    
                    """
        iEmail1= Email(id_email= iIDEmail, tipo_email= iTipoEmail, titulo= iTitulo, mensagem= iMensagem)
        iEmail1.save()