'''
Created on Sep 13, 2012

@author: spengler
'''

import logging
import os

from PIL                            import Image
from django.db.models               import get_model
from PyProject_GED                  import constantes
from django.conf                    import settings


class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def converteExtencaoImagem(self, vIDVersao, iIDExtencao):
        try:
            mVersao= get_model('documento', 'Versao')
            iDiretorioImagem= mVersao().obtemCaminhoArquivo(vIDVersao)
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
    
    def verificaSeImagemEhExportavel(self, vVersao):
        try:
            mVersao= get_model('documento', 'Versao')
            iDiretorioImagem= mVersao().obtemCaminhoArquivo(vVersao.id_versao)
            iExtencao= os.path.splitext(str(iDiretorioImagem))[1]
            if iExtencao.lower() in constantes.cntExtencaoImagemExportavel:
                iEhExportavel= True
            else:
                iEhExportavel= False
            return iEhExportavel
        except Exception, e:
            self.getLogger().error('Nao foi possivel verificar se imagem eh exportavel: ' + str(e))
            return False
    
    def deletaImagemTemporaria(self, vDiretorioImagem):
        try:
            os.remove(vDiretorioImagem)
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel criar a pasta temporaria: ' + str(e))
            return False
    
    def comprimeImagem(self, vVersao):
        try:
            mVersao= get_model('documento', 'Versao')
            iCaminhoArquivo= mVersao().obtemCaminhoArquivo(vVersao.id_versao)
            iExtencao = os.path.splitext(str(iCaminhoArquivo))[1]
            if iExtencao in constantes.cntExtencaoImagemComprimivel:
                iSmush= '%s/imagem/smush/smush.py' % settings.PROJECT_ROOT_PATH
                os.system('python %s --quiet %s' % (iSmush, iCaminhoArquivo))
            return True
        except Exception, e:
            self.getLogger().error('PyProject_GED.controle').error('Nao foi possivel comprimir imagens: ' + str(e))
            return False