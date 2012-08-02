# -*- coding: utf-8 -*- 

import logging
from django.conf                    import settings

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
        
    def obtemCaminhoVisualizar(self, vArquivo):
        try:
            iCaminho = vArquivo.replace('/home/diego/git/GED/src/PyProject_GED', '')
            return iCaminho
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemCaminhoVisualizar: ' + str(e))
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
            
    
