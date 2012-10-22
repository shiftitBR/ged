# -*- coding: utf-8 -*-
'''
Created on Oct 5, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                                  import models
from django.conf                                import settings

from PyProject_GED.autenticacao.models          import Usuario
from PyProject_GED                              import constantes
from PyProject_GED.servidor.objetos_auxiliares  import Importar as ImportarAuxiliar

import datetime
import simplejson
import logging
import SocketServer
import json
import os


class Servidor(models.Model):
    
    def iniciaSocket_TCP(self):
        try:      
            iServer = SocketServer.TCPServer((constantes.cntSocketTCPIP, constantes.cntSocketTCPPorta), Socket)
            iServer.serve_forever()
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os tipos de Indice: ' + str(e))
            return False
        
    def criaRespostaEmJSON(self, vPastaDestino, vIDUsuario=None, vLink=None):
        try:
            iResposta= {}
            iResposta['tipo']   = constantes.cntTipoMensagemJSONNormal
            iResposta['ip']     = constantes.cntServidorFTPIP
            iResposta['login']  = constantes.cntServidorFTPLogin
            iResposta['senha']  = constantes.cntServidorFTPSenha
            iResposta['pasta']  = vPastaDestino
            if vIDUsuario != None:
                iResposta['usuario']= vIDUsuario
            if vLink != None:
                iResposta['link']= vLink
            iJSON= json.dumps(iResposta)
            return iJSON
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a resposta para o cliente: ' + str(e))
            return False
        
class Socket(SocketServer.BaseRequestHandler):

    def handle(self):
        iJSONConectado= '{"tipo": %s, "mensagem": "Conectado"}' % constantes.cntTipoMensagemJSONNormal
        self.request.sendall(iJSONConectado + '\n')
        self.data = self.request.recv(1024).strip()
        iIPOrigem= self.client_address[0]
        iMensagemRecebida= self.data
        iJSONRecebido = simplejson.loads(iMensagemRecebida)
        iClasse = iJSONRecebido['classe']
        iEmail  = iJSONRecebido['usuario']
                
        if iClasse == constantes.cntClasseMensagemImportacao:
            iSenha  = iJSONRecebido['senha']
            iUsuario= Usuario().autenticaUsuario(iEmail, iSenha)
            if iUsuario != None:
                iImportacao= Importacao_FTP().criaImportacao_FTP(iUsuario, iIPOrigem)
                iPasta= '%s/%s' % (constantes.cntClasseMensagemImportacao, iImportacao.pasta_temporaria)
                iJSONResposta= Servidor().criaRespostaEmJSON(iPasta)
            else:
                iJSONResposta= '{"tipo": %s, "mensagem": "Usuario e Senha nao conferem!"}' % constantes.cntTipoMensagemJSONErro
        
        elif iClasse == constantes.cntClasseMensagemCadastro:
            iSenha  = iJSONRecebido['senha']
            iUsuario= Usuario().autenticaUsuario(iEmail, iSenha)
            if iUsuario != None:
                iPossuiCadastro= Cadastro_Biometria().verificaExistenciaDeCadastro(iUsuario)
                if not iPossuiCadastro:
                    iCadastro= Cadastro_Biometria().criaCadastroDeBiometria(iUsuario, iIPOrigem)
                    iPasta= '%s/%s' % (constantes.cntClasseMensagemCadastro, iCadastro.pasta_destino)
                    iJSONResposta= Servidor().criaRespostaEmJSON(iPasta, vIDUsuario= iCadastro.usuario.id)
                else:
                    iJSONResposta= '{"tipo": %s, "mensagem": "Usuario ja possui cadastro!"}' % constantes.cntTipoMensagemJSONErro
            else:
                iJSONResposta= '{"tipo": %s, "mensagem": "Usuario e Senha nao conferem!"}' % constantes.cntTipoMensagemJSONErro
        
        elif iClasse == constantes.cntClasseMensagemBiometria:
            print 'Biometria'
        
        self.request.sendall(iJSONResposta + '\n')

class Importacao_FTP(models.Model):
    id_importacao_ftp   = models.IntegerField(max_length=5, primary_key=True)
    usuario             = models.ForeignKey(Usuario, null= False)
    ip_origem           = models.CharField(max_length=20, null=False)
    pasta_temporaria    = models.CharField(max_length=200, null=False)
    data_importacao     = models.DateTimeField(null= True)
    
    class Meta:
        db_table= 'tb_importacao_ftp'
        verbose_name = 'Importação FTP'
        verbose_name_plural = 'Importações FTP'
    
    def __unicode__(self):
        return str(self.id_importacao_ftp)
    
    def save(self):  
        try:
            if len(Importacao_FTP.objects.order_by('-id_importacao_ftp')) > 0:   
                iUltimoRegistro = Importacao_FTP.objects.order_by('-id_importacao_ftp')[0] 
                self.id_importacao_ftp= iUltimoRegistro.pk + 1
            else:
                self.id_importacao_ftp= 1
            self.pasta_temporaria= str(self.id_importacao_ftp)
            super(Importacao_FTP, self).save()
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar importacao_ftp: ' + str(e))
            return False
    
    def criaImportacao_FTP(self, vUsuario, vIPOrigem):
        try:
            iImportacao                 = Importacao_FTP()
            iImportacao.usuario         = Usuario().obtemUsuario(vUsuario)
            iImportacao.ip_origem       = vIPOrigem
            iImportacao.data_importacao = str(datetime.datetime.today())[:19]
            iImportacao.save()
            return iImportacao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar importacao_ftp: ' + str(e))
            return False
        
    def criaRespostaEmJSON(self, vPastaDestino):
        try:
            iResposta= {}
            iResposta['tipo']   = constantes.cntTipoMensagemJSONNormal
            iResposta['ip']     = constantes.cntServidorFTPIP
            iResposta['login']  = constantes.cntServidorFTPLogin
            iResposta['senha']  = constantes.cntServidorFTPSenha
            iResposta['pasta']  = vPastaDestino
            iJSON= json.dumps(iResposta)
            return iJSON
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar a resposta para o cliente: ' + str(e))
            return False
    
    def obtemListaImportacoes(self, vUsuario):
        try:
            iListaImportacoes   = Importacao_FTP.objects.filter(usuario=vUsuario.id)
            iNumero = 0
            iListaAuxiliar      = []
            for Importar in iListaImportacoes:
                iCaminho            = settings.MEDIA_ROOT + "/documentos/ftp/" +Importar.pasta_temporaria
                for (path, dirs,files) in os.walk(iCaminho):
                    for iFile in files:
                        iImportarAux= ImportarAuxiliar()
                        iNumero                     = iNumero + 1
                        iImportarAux.numero         = iNumero
                        iImportarAux.caminho        = os.path.join(path, iFile)
                        iImportarAux.tamanho        = "%0.1f KB" % (os.path.getsize(iImportarAux.caminho)/(1024.0))
                        iImportarAux.nomeArquivo    = os.path.basename(iImportarAux.caminho)
                        iListaAuxiliar.append(iImportarAux)
            return iListaAuxiliar
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar obtem obtem Lista Importacoes: ' + str(e))
            return False

class Cadastro_Biometria(models.Model):
    id_cadastro_biometria   = models.IntegerField(max_length=5, primary_key=True)
    usuario                 = models.ForeignKey(Usuario, null= False)
    ip_origem               = models.CharField(max_length=20, null=False)
    pasta_destino           = models.CharField(max_length=200, null=False)
    data_importacao         = models.DateTimeField(null= True)
    
    class Meta:
        db_table= 'tb_cadastro_biometria'
        verbose_name = 'Cadastro de Biometria'
        verbose_name_plural = 'Cadastros de Biometria'
    
    def __unicode__(self):
        return str(self.id_cadastro_biometria)
    
    def save(self):  
        try:
            if len(Cadastro_Biometria.objects.order_by('-id_cadastro_biometria')) > 0:   
                iUltimoRegistro = Cadastro_Biometria.objects.order_by('-id_cadastro_biometria')[0] 
                self.id_cadastro_biometria= iUltimoRegistro.pk + 1
            else:
                self.id_cadastro_biometria= 1
            super(Cadastro_Biometria, self).save()
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel salvar cadastro de biometria: ' + str(e))
            return False
    
    def criaCadastroDeBiometria(self, vUsuario, vIPOrigem):
        try:
            iUsuario                    = Usuario().obtemUsuario(vUsuario)
            iCadastro                   = Cadastro_Biometria()
            iCadastro.usuario           = iUsuario
            iCadastro.ip_origem         = vIPOrigem
            iCadastro.pasta_destino     = str(iUsuario.empresa.id_empresa)
            iCadastro.data_importacao   = str(datetime.datetime.today())[:19]
            iCadastro.save()
            return iCadastro
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar cadastro de biometria: ' + str(e))
            return False
    
    def verificaExistenciaDeCadastro(self, vUsuario):
        try:
            iListaCadastros= Cadastro_Biometria.objects.filter(usuario= vUsuario)
            if len(iListaCadastros) > 0:
                iExisteCadastro= True
            else:
                iExisteCadastro= False
            return iExisteCadastro
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel verificar existencia de cadastro: ' + str(e))
            return False   