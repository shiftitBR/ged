
from django.test                                import TestCase

from models                                     import Empresa
from models                                     import Usuario
from models                                     import Tipo_de_Usuario

class Test(TestCase):
    
    def setUp(self):
        self.mokarEmpresa()
        self.mokarTipoUsuario()
        self.mokarUsuario()
        pass

    def tearDown(self):
        Empresa.objects.all().delete()
        Tipo_de_Usuario.objects.all().delete()
        Usuario.objects.all().delete()
        pass


    def testCriarEmpresa(self):
        iNome           = 'empresa_001'
        iBanco          = 'shift_ged'
        iPastaRaiz      = '/documentos/empresa_001/1'
        iEh_Ativo       = True
        iEmpresa        = Empresa(nome= iNome, banco= iBanco, pasta_raiz= iPastaRaiz, eh_ativo= iEh_Ativo)
        iEmpresa.save()
        self.assertEquals(iEmpresa.id_empresa, (Empresa.objects.filter(id_empresa= 3)[0].id_empresa))
        
    def testCriarTipoUsuario(self):
        iDescricao      = 'administador'
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario    = Tipo_de_Usuario(descricao= iDescricao, empresa= iEmpresa)
        iTipoUsuario.save()
        self.assertEquals(iTipoUsuario.id_tipo_usuario, (Tipo_de_Usuario.objects.filter(empresa= 1).filter(id_tipo_usuario= 5)[0].id_tipo_usuario))
        
    def testCriarUsuario(self):
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(empresa= iEmpresa.id_empresa)[0]
        iEh_Ativo       = True
        iUsuario        = Usuario(empresa= iEmpresa, tipo_usuario= iTipoUsuario, eh_ativo= iEh_Ativo)
        iUsuario.save()
        self.assertEquals(iUsuario.id, (Usuario.objects.filter(empresa= 1).filter(id= 13)[0].id))
    
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
        
        iDescricao      = 'usuario'
        iEmpresa        = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario_1  = Tipo_de_Usuario(descricao= iDescricao, empresa= iEmpresa)
        iTipoUsuario_1.save()
        
        iDescricao      = 'administador'
        iEmpresa        = Empresa.objects.filter(id_empresa= 2)[0]
        iTipoUsuario_2  = Tipo_de_Usuario(descricao= iDescricao, empresa= iEmpresa)
        iTipoUsuario_2.save()
        
        iDescricao      = 'usuario'
        iEmpresa        = Empresa.objects.filter(id_empresa= 2)[0]
        iTipoUsuario_2  = Tipo_de_Usuario(descricao= iDescricao, empresa= iEmpresa)
        iTipoUsuario_2.save()
        
    def mokarUsuario(self):
        iEmpresa_1      = Empresa.objects.filter(id_empresa= 1)[0]
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(empresa= iEmpresa_1.id_empresa).filter(descricao= 'administador')[0]
        iEh_Ativo       = True
        iUsuario_1      = Usuario(empresa= iEmpresa_1, tipo_usuario= iTipoUsuario, eh_ativo= iEh_Ativo)
        iUsuario_1.save()
        
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(empresa= iEmpresa_1.id_empresa).filter(descricao= 'usuario')[0]
        iEh_Ativo       = True
        iUsuario_2      = Usuario(empresa= iEmpresa_1, tipo_usuario= iTipoUsuario, eh_ativo= iEh_Ativo)
        iUsuario_2.save()
        
        iEmpresa_2      = Empresa.objects.filter(id_empresa= 2)[0]
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(empresa= iEmpresa_2.id_empresa).filter(descricao= 'usuario')[0]
        iEh_Ativo       = True
        iUsuario_3      = Usuario(empresa= iEmpresa_2, tipo_usuario= iTipoUsuario, eh_ativo= iEh_Ativo)
        iUsuario_3.save()
        
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(empresa= iEmpresa_2.id_empresa).filter(descricao= 'usuario')[0]
        iEh_Ativo       = True
        iUsuario_4      = Usuario(empresa= iEmpresa_2, tipo_usuario= iTipoUsuario, eh_ativo= iEh_Ativo)
        iUsuario_4.save()