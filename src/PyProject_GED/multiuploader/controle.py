# -*- coding: utf-8 -*- 

import logging

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    
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
            return False
        