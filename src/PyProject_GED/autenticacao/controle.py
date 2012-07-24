'''
Created on Jul 24, 2012

@author: Shift IT | www.shiftit.com.br
'''

# -*- coding: utf-8 -*- 

from models                             import Empresa, Tipo_de_Usuario   
from PyProject_GED.seguranca.models     import Pasta
from PyProject_GED.indice.models        import Tipo_de_Indice
from PyProject_GED.documento.models     import Tipo_de_Documento

import threading
import logging

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def criaEmpresa(self, vIDEmpresa):
        class ThreadClass(threading.Thread):
            def run(self):
                iEmpresa= Empresa.objects.filter(id_empresa= vIDEmpresa)[0]
                iPastaRaiz= self.criaPasta(iEmpresa, 'Pasta Raiz')
                self.criaPasta(vIDEmpresa, 'Modelos', iPastaRaiz)
                self.atualizaEmpresa(iEmpresa, iPastaRaiz.diretorio)
                self.criaTipoUsuario(iEmpresa, 'Administrador')
                self.criaTipoIndice(iEmpresa, 'String')
                self.criaTipoDocumento(iEmpresa, 'Modelo')
        
        try:
            iThread = ThreadClass()
            iThread.start()
            return True
        except Exception, e:
            print str(e)
            self.getLogger().error('Nao foi possivel criar a Empresa: ' + str(e))
            return False
        
    def atualizaEmpresa(self, vEmpresa, vDiretorioRaiz):
        try:
            vEmpresa.pasta_raiz= vDiretorioRaiz
            vEmpresa.save()
            return vEmpresa
        except Exception, e:
            print str(e)
            self.getLogger().error('Nao foi possivel atualizar a Empresa: ' + str(e))
            return False
    
    def criaPasta(self, vEmpresa, vNomePasta, vPastaPai=None):
        try:
            iPasta= Pasta()
            iPasta.nome= vNomePasta
            iPasta.empresa= vEmpresa
            if vPastaPai != None:
                iPasta.pasta_pai= vPastaPai
            iPasta.save()
            return iPasta
        except Exception, e:
            print str(e)
            self.getLogger().error('Nao foi possivel criar as pastas: ' + str(e))
            return False
    
    def criaTipoUsuario(self, vEmpresa, vDescricao):
        try:
            iTipoUsuario= Tipo_de_Usuario()
            iTipoUsuario.id_tipo_usuario= 1
            iTipoUsuario.descricao= vDescricao
            iTipoUsuario.empresa= vEmpresa
            iTipoUsuario.save()
            return iTipoUsuario
        except Exception, e:
            print str(e)
            self.getLogger().error('Nao foi possivel criar os tipos de usuario: ' + str(e))
            return False
    
    def criaTipoIndice(self, vEmpresa, vDescricao):
        try:
            iTipoDeIndice= Tipo_de_Indice()
            iTipoDeIndice.descricao= vDescricao
            iTipoDeIndice.empresa= vEmpresa
            iTipoDeIndice.save()
            return iTipoDeIndice
        except Exception, e:
            print str(e)
            self.getLogger().error('Nao foi possivel criar os tipos de Indice: ' + str(e))
            return False
    
    def criaTipoDocumento(self, vEmpresa, vDescricao):
        try:
            iTipoDeDocumento= Tipo_de_Documento()
            iTipoDeDocumento.descricao= vDescricao
            iTipoDeDocumento.eh_nativo= True
            iTipoDeDocumento.empresa= vEmpresa
            iTipoDeDocumento.save()
            return iTipoDeDocumento
        except Exception, e:
            print str(e)
            self.getLogger().error('Nao foi possivel criar os tipos de Documento: ' + str(e))
            return False