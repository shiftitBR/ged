
from django.test                                import TestCase

from autenticacao.models        import Empresa #@UnresolvedImport
from autenticacao.models        import Usuario #@UnresolvedImport
from seguranca.models           import Pasta #@UnresolvedImport
from multiuploader.models       import MultiuploaderImage #@UnresolvedImport

from models                     import Tipo_de_Documento
from models                     import Documento
from models                     import Estado_da_Versao
from models                     import Versao

import autenticacao.tests as TesteAutencicacao#@UnresolvedImport

class Test(TestCase):
    
    def setUp(self):
        
        pass
    
    
    def tearDown(self):
        Empresa.objects.all().delete()
        Usuario.objects.all().delete()
        pass
    
    
    
    
    
    
    
    #-----------------------------------------------------MOKS---------------------------------------------------