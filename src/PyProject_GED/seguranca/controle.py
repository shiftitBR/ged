# -*- coding: utf-8 -*- 

import logging
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