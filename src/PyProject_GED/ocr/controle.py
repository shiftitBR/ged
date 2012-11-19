'''
Created on Aug 9, 2012

@author: Shift IT | www.shiftit.com.br
'''

# -*- coding: utf-8 -*- 


from Image                  import open as OpenImage
from tesseract              import image_to_string

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

import logging
import os
import uno
import constantes #@UnresolvedImport
import unicodedata
import pytiff #@UnresolvedImport

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def executaOCR(self, vVersao):
        try:
            iExtencao= os.path.splitext(str(vVersao.upload.image))[1].lower()
            if iExtencao in constantes.cntOCRExtencoesPDF:
                iTexto= self.obtemTextoDoPDF(vVersao)
            elif iExtencao in constantes.cntOCRExtencoesImagens:
                iTexto= self.obtemTextoDaImagem(vVersao)
            else:
                iTexto= None
            
            if iTexto != None:
                iExecutou= len(iTexto) > 0
            else:
                iExecutou= None
                iTexto= 'Nao foi possivel passar o OCR'
            return iExecutou
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter texto da imagem: ' + str(e))
            return False
    
    def obtemTextoDaImagem(self, vVersao):
        try:
            iEnderecoImagem= vVersao.upload.image
            try:
                iTexto= image_to_string(OpenImage(iEnderecoImagem))
                self.criaArquivoOCR(iEnderecoImagem, iTexto)
            except:
                iTexto = None
            return iTexto
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter texto da imagem: ' + str(e))
            return False
    
    def obtemTextoDoPDF(self, vVersao):
        try:
            iEnderecoDocumento= vVersao.upload.image
            try:
                iTexto= self.lePDF(str(iEnderecoDocumento))
                self.criaArquivoOCR(iEnderecoDocumento, iTexto)
            except:
                iTexto = None
            return iTexto
        except Exception, e:
            self.getLogger().error('Nao foi possivel buscar texto do pdf: ' + str(e))
            return False
    
    def buscaEmConteudoDoDocumento(self, vVersao, vString):
        try:
            iExtencao= os.path.splitext(str(vVersao.upload.image))[1].lower()
            iEncontrou= False
            if iExtencao in constantes.cntOCRExtencoesDocumentos:
                iEncontrou= self.buscaTextoNoDocumento(vString, vVersao)
            elif iExtencao in constantes.cntOCRExtencoesImagens or \
                 iExtencao in constantes.cntOCRExtencoesPDF or \
                 iExtencao in constantes.cntOCRExtencoesTextos:
                iEncontrou= self.buscaTextoNoTXT(vString, vVersao= vVersao)
            return iEncontrou
        except Exception, e:
            self.getLogger().error('Nao foi possivel buscar texto no documento: ' + str(e))
            return False
    
    def buscaTextoNoDocumento(self, vTexto, vVersao):
        try:
            local = uno.getComponentContext()
            resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
            context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
            iEnderecoDocumento= str(vVersao.upload.image)
            document = desktop.loadComponentFromURL("file://%s" % iEnderecoDocumento ,"_blank", 0, ())
            search = document.createSearchDescriptor()
            search.SearchString = vTexto
            search.SearchCaseSensitive = False     
            found = document.findFirst( search )
            document.dispose()
            return found != None
        except Exception, e:
            self.getLogger().error('Nao foi possivel buscar texto do documento: ' + str(e))
            return False
        
    def buscaTextoNoTXT(self, vTexto, vVersao=None, vEnderecoArquivoTXT=None):
        try:
            if vVersao != None:
                iEnderecoDocumento= str(vVersao.upload.image)
            else:
                iEnderecoDocumento= vEnderecoArquivoTXT
            iNomeArquivo, iExtencaoArquivo = os.path.splitext(str(iEnderecoDocumento))
            if iExtencaoArquivo.lower() != 'txt':
                iEnderecoDocumento= '%s.%s' % (iNomeArquivo, constantes.cntOCRExtencaoDocumentoTexto)
            iArquivo = open(str(iEnderecoDocumento),"r")
            iTextoArquivo = iArquivo.read().lower()
            iArquivo.close()
            iLocalizar = unicodedata.normalize('NFKD', vTexto.lower()).encode('ascii', 'ignore')
            iIndex = iTextoArquivo.find(iLocalizar)
            return iIndex > -1
        except Exception, e:
            self.getLogger().error('Nao foi possivel buscar texto do txt: ' + str(e))
            return False
    
    def lePDF(self, path):
        try:
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
            fp = file(path, 'rb')
            process_pdf(rsrcmgr, device, fp)
            fp.close()
            device.close()
            str = retstr.getvalue()
            retstr.close()
            return str
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter texto do pdf: ' + str(e))
            return False
    
    def criaArquivoOCR(self, vEnderecoArquivoPai, vTexto):
        try:
            iNomeArquivo = os.path.splitext(str(vEnderecoArquivoPai))[0]
            iEnderecoArquivoOCR= '%s.%s' % (iNomeArquivo, constantes.cntOCRExtencaoDocumentoTexto)
            iArquivo = open('%s.%s' % (iNomeArquivo, constantes.cntOCRExtencaoDocumentoTexto),"w")
            iArquivo.write(vTexto)
            iArquivo.close()
            return iEnderecoArquivoOCR
        except Exception, e:
            self.getLogger().error('Nao foi possivel criar arquivo txt: ' + str(e))
            return False