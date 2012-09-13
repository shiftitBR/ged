'''
Created on Sep 13, 2012

@author: spengler
'''

import logging
from PIL import Image
from PyProject_GED.documento.models import Versao
import os
from PyProject_GED import constantes


class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def converteExtencaoImagem(self, vIDVersao, iIDExtencao):
        try:
            iDiretorioImagem= Versao().obtemCaminhoArquivo(vIDVersao)
            if iIDExtencao == constantes.cntExtencaoImagemJPG:
                iExtencao= 'jpg'
            elif iIDExtencao == constantes.cntExtencaoImagemPNG:
                iExtencao= 'png'
            elif iIDExtencao == constantes.cntExtencaoImagemBMP:
                iExtencao= 'bmp'
            elif iIDExtencao == constantes.cntExtencaoImagemTIF:
                iExtencao= 'tif'
                
            iDiretorioImagemSemExtencao= os.path.splitext(str(iDiretorioImagem))[0]
            iDiretorioImagemNovo= '%s.%s' % (iDiretorioImagemSemExtencao, iExtencao)
            im = Image.open(iDiretorioImagem)
            im.save(iDiretorioImagemNovo) 
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel criar pastas: ' + str(e))
            return False