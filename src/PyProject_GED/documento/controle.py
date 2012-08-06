# -*- coding: utf-8 -*- 

import logging
import datetime

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    
    def obtemIDPastaArvore(self, vCaminho):
        try:
            iLista = vCaminho.split('/')
            if vCaminho[len(vCaminho)-1] != '/': #sem / no final
                iIDPasta= iLista[len(iLista)-1]
            else :  #com / no final 
                iIDPasta= iLista[len(iLista)-2]
            return iIDPasta
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemIDPastaArvore: ' + str(e))
            return False
        
        
    def obtemPermissao(self, vIDUsuario, vIDFuncao):
        try:
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemPermissao: ' + str(e))
            return False
        
    def ehVisualizavel(self, vNome):
        try:
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemPermissao: ' + str(e))
            return False
    
    def formataData(self, vDataString):
        try:
            iListaData= vDataString.split('/')
            iData= datetime.datetime(int(iListaData[2]), int(iListaData[1]), int(iListaData[0]), 00, 00, 00)
            return iData
        except Exception, e:
            self.getLogger().error('Nao foi possivel formatar a data: ' + str(e))
            return False
    
