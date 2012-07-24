# -*- coding: utf-8 -*- 

import logging
from PyProject_GED          import constantes
from models                 import Pasta     

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger

    def obtemDiretorioUpload(self, vIDPasta):
        try :
            iPasta = Pasta.objects.filter(id_pasta= vIDPasta)[0]
            return iPasta.diretorio
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemDiretorioUpload: ' + str(e))
            return False
    
    def montaDiretorioPasta(self, vIDEmpresa, vIDPasta, vIDPastaPai=None):
        try :
            if vIDPastaPai == None:
                iDiretorio= '%s/%s' % ((constantes.cntConfiguracaoDiretorioDocumentos % vIDEmpresa), vIDPasta)
            else:
                iPastaPai = Pasta.objects.filter(id_pasta= vIDPastaPai)[0]
                iDiretorio= '%s/%s' % (iPastaPai, vIDPasta)
            return iDiretorio
        except Exception, e:
            self.getLogger().error('Nao foi possivel omontar o Diretorio da Pasta: ' + str(e))
            return False
