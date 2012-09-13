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
            iListaDiretorio= iDiretorioImagemSemExtencao.split('/')
            iNomeArquivo= iListaDiretorio[len(iListaDiretorio)-1:][0]
            iPastaImagem= iDiretorioImagemSemExtencao[:len(iDiretorioImagemSemExtencao)-len(iNomeArquivo)]
            iPastaTemporario= '%s/temp' % iPastaImagem[:len(iPastaImagem)-1]
            self.criaPastaTemporaria(iPastaTemporario)
            iDiretorioImagemNovo= '%s/%s.%s' % (iPastaTemporario, iNomeArquivo, iExtencao)
            iImagem = Image.open(iDiretorioImagem)
            iImagem.save(iDiretorioImagemNovo) 
            return iDiretorioImagemNovo
        except Exception, e:
            self.getLogger().error('Nao foi possivel converter a imagem: ' + str(e))
            return False
    
    def criaPastaTemporaria(self, vPastaTemporario):
        try:
            if not os.path.exists(vPastaTemporario):
                os.system('mkdir %s' % vPastaTemporario)
        except Exception, e:
            self.getLogger().error('Nao foi possivel criar a pasta temporaria: ' + str(e))
            return False