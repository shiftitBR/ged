'''
Created on Aug 21, 2012

@author: Shift IT | www.shiftit.com.br
'''

import logging
from PyProject_GED.scanner.core._imagescanner   import ImageScanner

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def executaScanner(self, vIDScanner=None):
        try:
            iscanner = ImageScanner()
            
            scanners = iscanner.list_scanners()
            
            print '>>>>>>>>>>>>>>>>>>>'
            #print scanners
            print '<<<<<<<<<<<<<<<<<<<'
            scanner = scanners[1]
            
            iImagem= scanner.scan()
            print type(iImagem)
            print iImagem
#            iImagem.save('/home/spengler/Git/GED/PyProject_GED/src/PyProject_GED/media/documentos/empresa_001/7/8/teste.tif', "TIFF")
            iImagem.save('/home/webapps/GED/media/documentos/empresa_005/9/10/', "TIFF")
            print '||||||||||||||||||||||||||||||||||||||||||||||||'
            print 'salvou'
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel executar o scanner: ' + str(e))
            return False