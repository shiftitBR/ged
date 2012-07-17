'''
Created on Jan 20, 2012

@author: spengler
'''

import logging
import os
import locale
import constantes


from django.conf    import settings
from multiAdmin     import MultiDBModelAdmin

class Controle(object):
    
    oLogger = logging.getLogger(__name__)
    oBanco  = constantes.cntConfiguracaoBancoPadrao
    
    def inicializaAplicacao(self):
        try:
            locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
            self.criaLog()
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel inicializar a classe Controle: ' + str(e))
            return False
        
    def setLogger(self, vLogger):
        self.oLogger= vLogger
        
    def getLogger(self):
        return self.oLogger
    
    def setBanco(self, vBanco):
        try:
            self.oBanco= vBanco
            MultiDBModelAdmin.using= vBanco
        except Exception, e:
            self.getLogger().error('Nao foi possivel setar o Banco: ' + str(e))
            return False

    def getBanco(self):
        try:
            return self.oBanco
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter o Banco: ' + str(e))
            return False
    
    def criaEmpresa(self, vIDEmpresa):
        try:
            iDiretorioRaiz= settings.PROJECT_ROOT_PATH
            iFabFile= '%s/fabfile.py' % iDiretorioRaiz
            os.system('fab -f %s cria_empresa:%s,%s' % (iFabFile, int(vIDEmpresa), iDiretorioRaiz))
            return True
        except Exception, e:
            print str(e)
            self.getLogger().error('Nao foi possivel criar a Empresa: ' + str(e))
            return False
    
    def criaLog(self):
        try:
            iLogFile= settings.PROJECT_ROOT_PATH + os.path.sep + 'log' + os.path.sep + 'ged.log'
            iFormat = '[%(asctime)-15s] [%(levelname)-8s] [%(module)s] (%(funcName)s, '\
                      'linha: %(lineno)d) {%(message)s}'
            logging.basicConfig(level=logging.DEBUG, filename=iLogFile, format=iFormat)
            return True
        except:
            return False