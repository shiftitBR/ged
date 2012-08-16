'''
Created on Jul 24, 2012

@author: Shift IT | www.shiftit.com.br
'''

# -*- coding: utf-8 -*- 

from PyProject_GED  import constantes

import logging
import os


class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def criaPasta(self, vIDEmpresa, vIDPastaRaiz, vIDPastaModelo):
        try:
            iDiretorioEmpresa= constantes.cntConfiguracaoDiretorioDocumentos % vIDEmpresa
            os.system('mkdir %s' % iDiretorioEmpresa) 
            os.system('mkdir %s/%s' % (iDiretorioEmpresa, vIDPastaRaiz)) 
            os.system('mkdir %s/%s/%s' % (iDiretorioEmpresa, str(vIDPastaRaiz), str(vIDPastaModelo)))
            self.getLogger().warning('Diretorio_Empresa: '+iDiretorioEmpresa)
        except Exception, e:
            self.getLogger().error('Nao foi possivel criar pastas: ' + str(e))
            return False