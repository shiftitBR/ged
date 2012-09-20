# -*- coding: utf-8 -*- 

from django.conf                    import settings

import logging
import datetime
import constantes #@UnresolvedImport

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
            iCaminho = vArquivo.replace(settings.PROJECT_ROOT_PATH, '')
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
        
    def tipoVisualizavel(self, vNome):
        try:
            iListaImagem= ['png', 'jpg', 'bmp']
            iListaNome= vNome.split('.')
            iExt= iListaNome[1]
            iTipo= constantes.cntTipoVisualizacaoOutro
            if iExt == 'pdf':
                iTipo= constantes.cntTipoVisualizacaoPDF
            else:
                for i in range(len(iListaImagem)):
                    if iExt == iListaImagem[i]:
                        iTipo= constantes.cntTipoVisualizacaoImagem 
            return iTipo 
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemPermissao: ' + str(e))
            return False
            
    def obtemListaNomesUsuarios(self, vLista):
        try:
            iListaNome=''
            for i in range (len(vLista)):
                iNomeUsuario= vLista[i].first_name + ' ' + vLista[i].last_name + ' - %04d' % vLista[i].id
                if iListaNome=='':
                    iListaNome= iListaNome + '"'+iNomeUsuario+'"'
                else:
                    iListaNome= iListaNome + ',"'+iNomeUsuario+'"'
            iListaNome= '[' + iListaNome + ']'
            return iListaNome
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemListaNomesUsuarios: ' + str(e))
    
    def formataData(self, vData):
        try:
            if type(vData) == str:
                iListaData= vData.split('/')
                iData= datetime.datetime(int(iListaData[2]), int(iListaData[1]), int(iListaData[0]), 00, 00, 00)
            else:
                if vData not in (None, ''):
                    iData= vData.strftime("%d/%m/%Y")
                else:
                    iData= vData
            return iData
        except Exception, e:
            self.getLogger().error('Nao foi possivel formatar a data: ' + str(e))
            return False
        
