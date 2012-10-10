# -*- coding: utf-8 -*-
'''
Created on Oct 5, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models

import logging
import socket
import SocketServer
import json
from PyProject_GED.autenticacao.models import Usuario
from PyProject_GED import constantes
import datetime
import simplejson


class Servidor(models.Model):
    
    def iniciaSocket_TCP(self):
        try:      
            iServer = SocketServer.TCPServer((constantes.cntSocketTCPIP, constantes.cntSocketTCPPorta), Socket)
            iServer.serve_forever()
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os tipos de Indice: ' + str(e))
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
        
class Socket(SocketServer.BaseRequestHandler):

    def handle(self):
        iJSONConectado= '{"tipo": %s, "mensagem": "Conectado"}' % constantes.cntTipoMensagemJSONNormal
        self.request.sendall(iJSONConectado)
        self.data = self.request.recv(1024).strip()
        iIPOrigem= self.client_address[0]
        iMensagemRecebida= self.data
        iJSONRecebido = simplejson.loads(iMensagemRecebida)
        iEmail= iJSONRecebido['usuario']
        iSenha= iJSONRecebido['senha']
        iUsuario= Usuario().autenticaUsuario(iEmail, iSenha)
        if iUsuario != None:
            iImportacao= Importacao_FTP().criaImportacao_FTP(iUsuario, iIPOrigem)
            iJSONResposta= Servidor().criaRespostaEmJSON(iImportacao.pasta_temporaria)
        else:
            iJSONResposta= '{"tipo": %s, "mensagem": "Usuario e Senha nao conferem!"}' % constantes.cntTipoMensagemJSONErro
        self.request.sendall(iJSONResposta)

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
            iImportacao.usuario         = vUsuario
            iImportacao.ip_origem       = vIPOrigem
            iImportacao.data_importacao = str(datetime.datetime.today())[:19]
            iImportacao.save()
            return iImportacao
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar importacao_ftp: ' + str(e))
            return False