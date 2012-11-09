'''
Created on Jul 18, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.core                                    import mail
from django.conf                                    import settings

from PyProject_GED.envioemail.objetos_auxiliares    import Arquivo as ArquivoAux
from PyProject_GED.imagem.controle                  import Controle as ImagemControle
from PyProject_GED                                  import constantes

import logging
import os

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def enviarEmail(self, vTitulo, vTexto, vEmailDestino, vEmailRemetente):
        try:
            if settings.EMAIL:
                mail.send_mail(
                    subject=vTitulo,
                    message=vTexto,
                    from_email=vEmailRemetente,
                    recipient_list=[vEmailDestino],
                    )
            return True
        except Exception, e:
            self.getLogger().error('Nao foi possivel enviar email: ' + str(e))
            return False
        
    def obtemArquivoAuxiliar(self, vVersao):
        try:
            iArquivo = ArquivoAux()
            iArquivo.id_versao  = vVersao.id_versao
            iArquivo.protocolo  = vVersao.protocolo
            iArquivo.assunto    = vVersao.documento.assunto
            iArquivo.nome       = vVersao.upload.filename
            iArquivo.img        = ImagemControle().verificaSeImagemEhExportavel(vVersao)
            iArquivo.pdf        = False
            return iArquivo
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtem ArquivoAuxiliar: ' + str(e))
            return False
        
    def obtemNovoNomeArquivo(self, vCaminho, vExtensao):
        try:
            iDiretorioImagemSemExtencao= os.path.splitext(str(vCaminho))[0]
            iListaDiretorio= iDiretorioImagemSemExtencao.split('/')
            iNomeArquivo= iListaDiretorio[len(iListaDiretorio)-1:][0]
            if vExtensao == constantes.cntExtencaoImagemJPG:
                iExtensao= 'jpg'
            elif vExtensao == constantes.cntExtencaoImagemPNG:
                iExtensao= 'png'
            elif vExtensao == constantes.cntExtencaoImagemBMP:
                iExtensao= 'bmp'
            elif vExtensao == constantes.cntExtencaoImagemTIF:
                iExtensao= 'tif' 
            elif iExtensao == constantes.cntExtensaoImagemPDF: 
                iExtensao= 'pdf'
            iNomeNovo= '%s.%s' % (iNomeArquivo, iExtensao)
            return iNomeNovo
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtemNovoNomeArquivo: ' + str(e))
            return False