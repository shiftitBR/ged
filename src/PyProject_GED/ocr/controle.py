'''
Created on Aug 9, 2012

@author: Shift IT | www.shiftit.com.br
'''

# -*- coding: utf-8 -*- 

from PyProject_GED          import constantes
from Image                  import open as OpenImage
from tesseract              import image_to_string
from django.db.models       import get_model

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

import logging
import os
import uno

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    mVersao= get_model('documento', 'Versao')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def executaOCR(self, vVersao):
        try:
            iExtencao= os.path.splitext(str(vVersao.upload.image))[1].lower()
            if iExtencao in constantes.cntOCRExtencoesPDF:
                iTexto= self.obtemTextoDoPDF(vVersao.id_versao)
                iExecutou= len(iTexto) > 0
            elif iExtencao in constantes.cntOCRExtencoesImagens:
                iTexto= self.obtemTextoDaImagem(vVersao.id_versao)
                iExecutou= len(iTexto) > 0
            else:
                iTexto= 'Nao foi possivel passar o OCR'
                iExecutou= None
            return iExecutou
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter texto da imagem: ' + str(e))
            return False
    
    def obtemTextoDaImagem(self, vIDVersao):
        try:
            iEnderecoImagem= self.mVersao().obtemCaminhoArquivo(vIDVersao)
            iTexto= image_to_string(OpenImage(iEnderecoImagem))
            self.criaArquivoOCR(iEnderecoImagem, iTexto)
            return iTexto
        except Exception, e:
            self.getLogger().error('Nao foi possivel obter texto da imagem: ' + str(e))
            return False
    
    def obtemTextoDoPDF(self, vIDVersao):
        try:
            iEnderecoDocumento= self.mVersao().obtemCaminhoArquivo(vIDVersao)
            iTexto= self.lePDF(str(iEnderecoDocumento))
            self.criaArquivoOCR(iEnderecoDocumento, iTexto)
            return iTexto
        except Exception, e:
            self.getLogger().error('Nao foi possivel buscar texto do pdf: ' + str(e))
            return False
    
    def buscaEmConteudoDoDocumento(self, vVersao, vString):
        try:
            iExtencao= os.path.splitext(str(vVersao.upload.image))[1].lower()
            if iExtencao in constantes.cntOCRExtencoesDocumentos:
                iEncontrou= self.buscaTextoNoDocumento(vVersao.id_versao, vString)
            else:
                iEncontrou= self.buscaTextoNoTXT(vString, vIDVersao= vVersao.id_versao)
            return iEncontrou
        except Exception, e:
            self.getLogger().error('Nao foi possivel buscar texto no documento: ' + str(e))
            return False
    
    def buscaTextoNoDocumento(self, vIDVersao, vTexto):
        try:
            local = uno.getComponentContext()
            resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
            context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
            iEnderecoDocumento= self.mVersao().obtemCaminhoArquivo(vIDVersao)
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
        
    def buscaTextoNoTXT(self, vTexto, vIDVersao=None, vEnderecoArquivoTXT=None):
        try:
            if vIDVersao != None:
                iEnderecoDocumento= self.mVersao().obtemCaminhoArquivo(vIDVersao)
            else:
                iEnderecoDocumento= vEnderecoArquivoTXT
            iNomeArquivo, iExtencaoArquivo = os.path.splitext(str(iEnderecoDocumento))
            if iExtencaoArquivo.lower() != 'txt':
                iEnderecoDocumento= '%s.%s' % (iNomeArquivo, constantes.cntOCRExtencaoDocumentoTexto)
            iArquivo = open(str(iEnderecoDocumento),"r")
            iTexto = iArquivo.read().lower()
            iArquivo.close()
            iLocalizar = vTexto.lower()
            iIndex = iTexto.find(iLocalizar)
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