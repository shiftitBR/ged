# -*- coding: utf-8 -*- 

import logging
from models                 import Pasta     
from PyProject_GED          import oControle

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger


    def obtemDiretorioUpload(self):
        iPasta = Pasta.objects.filter(id_pasta= oControle.getIDPasta())[0]
        return iPasta.diretorio