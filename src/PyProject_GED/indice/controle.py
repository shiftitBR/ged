# -*- coding: utf-8 -*- 

import logging

from models                 import Indice  
from models                 import Indice_Versao_Valor
from documento.models       import Versao #@UnresolvedImport

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def salvaValorIndice(self, vValor, vIDIndice, vIDVersao):
        try:
            iIndice         = Indice.objects.filter(id_indice= vIDIndice)[0]
            iVersao         = Versao.objects.filter(id_versao= vIDVersao)[0]
            
            iIndice_Versao_Valor        = Indice_Versao_Valor()
            iIndice_Versao_Valor.indice = iIndice
            iIndice_Versao_Valor.versao = iVersao
            iIndice_Versao_Valor.valor  = vValor
            iIndice_Versao_Valor.save()
            return iVersao
        except Exception, e:
            self.getLogger().error('Nao foi possivel salvar a Versao do Documento: ' + str(e))
            return False