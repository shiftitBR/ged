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
import shutil
from PyProject_GED.multiuploader.models import MultiuploaderImage


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
    
    def copiaArquivo(self, vArquivo, vPastaDestino):
        try:      
            iCount= 0
            iNomeArquivo = os.path.basename(vArquivo)
            iNomeArquivoSemExtencao, iExtencaoArquivo = os.path.splitext(iNomeArquivo)
            iArquivoDestino = os.path.join(vPastaDestino, iNomeArquivo)
            while os.path.exists(iArquivoDestino):
                iCount += 1
                iArquivoDestino = os.path.join(vPastaDestino, '%s_%d%s' % (iNomeArquivoSemExtencao, iCount, iExtencaoArquivo))
            iNomeArquivoDestino= os.path.basename(iArquivoDestino)
            shutil.move(vArquivo, iArquivoDestino)
            return iNomeArquivoDestino
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel copiar o arquivo: ' + str(e))
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
                
        if iClasse == constantes.cntClasseMensagemImportacao:
            iJSONResposta= self.importacaoDeArquivos(iJSONRecebido, iIPOrigem)
        elif iClasse == constantes.cntClasseMensagemLogin:
            iJSONResposta= self.loginViaBiometria(iJSONRecebido)
        elif iClasse == constantes.cntClasseMensagemCadastro:
            iJSONResposta= self.cadastroDeBiometria(iJSONRecebido, iIPOrigem)     
        elif iClasse == constantes.cntClasseMensagemConfirmacao:
            iJSONResposta= self.confirmacaoDoCadastroDeBiometria(iJSONRecebido, iIPOrigem)
            
        if iJSONResposta == False:
            iJSONResposta= '{"tipo": %s, "mensagem": "Ocorreu um erro desconhecido!"}' % constantes.cntTipoMensagemJSONErro 
            
        self.request.sendall(iJSONResposta + '\n')
    
    def cadastroDeBiometria(self, vJSONRecebido, vIPOrigem):
        try:
            iSenha  = vJSONRecebido['senha']
            iEmail  = vJSONRecebido['usuario']
            iUsuario= Usuario().autenticaUsuario(iEmail, iSenha)
            if iUsuario != None:
                iCadastroExistente= Cadastro_Biometria().obtemCadastroDeBiometria(iUsuario)
                if iCadastroExistente == None:
                    iCadastro= Cadastro_Biometria().criaCadastroDeBiometria(iUsuario, vIPOrigem, False)
                    iPasta= '%s/%s' % (constantes.cntClasseMensagemCadastro, iCadastro.pasta_destino)
                    iJSONResposta= Servidor().criaRespostaEmJSON(iPasta, vIDUsuario= iCadastro.usuario.id)
                    iCadastro.clean()
                else:
                    iJSONResposta= '{"tipo": %s, "mensagem": "Usuario ja possui cadastro!"}' % constantes.cntTipoMensagemJSONErro
            else:
                iJSONResposta= '{"tipo": %s, "mensagem": "Usuario e Senha nao conferem!"}' % constantes.cntTipoMensagemJSONErro
            return iJSONResposta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel cadastrar biometria: ' + str(e))
            return False
    
    def confirmacaoDoCadastroDeBiometria(self, vJSONRecebido, vIPOrigem):
        try:
            iEmail  = vJSONRecebido['usuario']
            iUsuario= Usuario().obtemUsuarioPeloEmail(iEmail)
            iTipo = vJSONRecebido['tipo']
            if str(iTipo) == constantes.cntTipoMensagemJSONNormal:
                Cadastro_Biometria().criaCadastroDeBiometria(iUsuario, vIPOrigem)
                iJSONResposta= '{"tipo": %s, "mensagem": "Cadastro efetuado com sucesso"}' % constantes.cntTipoMensagemJSONNormal
                
            else:
                iJSONResposta= '{"tipo": %s, "mensagem": "Erro ao efetuar o cadastro"}' % constantes.cntTipoMensagemJSONErro
            return iJSONResposta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel confirmar o cadastrar de biometria: ' + str(e))
            return False
        
    def loginViaBiometria(self, vJSONRecebido):
        try:
            iEmail  = vJSONRecebido['usuario']
            iUsuario= Usuario().obtemUsuarioPeloEmail(iEmail)
            if iUsuario != None:
                if iUsuario.is_active:
                    if iUsuario.empresa.eh_ativo:
                        iCadastro= Cadastro_Biometria().obtemCadastroDeBiometria(iUsuario)
                        if iCadastro != None:
                            iPasta= '%s/%s' % (constantes.cntClasseMensagemCadastro, iCadastro.pasta_destino)
                            iLink = Usuario().obtemURLDeAutenticacao(iEmail)
                            iJSONResposta= Servidor().criaRespostaEmJSON(iPasta, iUsuario.id, iLink)
                        else:
                            iJSONResposta= '{"tipo": %s, "mensagem": "Este usuario nao possui cadastro!"}' % constantes.cntTipoMensagemJSONErro
                    else:
                        iJSONResposta= '{"tipo": %s, "mensagem": "A empresa esta inativa!"}' % constantes.cntTipoMensagemJSONErro
                else:
                    iJSONResposta= '{"tipo": %s, "mensagem": "O usuario esta inativo!"}' % constantes.cntTipoMensagemJSONErro
            else:
                iJSONResposta= '{"tipo": %s, "mensagem": "Usuario inexistente!"}' % constantes.cntTipoMensagemJSONErro
            return iJSONResposta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel logar via biometria: ' + str(e))
            return False
    
    def importacaoDeArquivos(self, vJSONRecebido, vIPOrigem):
        try:
            iSenha  = vJSONRecebido['senha']
            iEmail  = vJSONRecebido['usuario']
            iUsuario= Usuario().autenticaUsuario(iEmail, iSenha)
            if iUsuario != None:
                iImportacao= Importacao_FTP().criaImportacao_FTP(iUsuario, vIPOrigem)
                iPasta= '%s/%s' % (constantes.cntClasseMensagemImportacao, iImportacao.pasta_temporaria)
                iJSONResposta= Servidor().criaRespostaEmJSON(iPasta)
            else:
                iJSONResposta= '{"tipo": %s, "mensagem": "Usuario e Senha nao conferem!"}' % constantes.cntTipoMensagemJSONErro
            return iJSONResposta
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel importar os arquivos: ' + str(e))
            return False
            
            
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
            iDiretorioArquivo  = '%s/%s/%s' % (constantes.cntImportacaoFTPPastaRaiz, 
                                                    constantes.cntClasseMensagemImportacao, 
                                                    self.pasta_temporaria)
            os.system('mkdir %s' % iDiretorioArquivo) 
            os.system('chown trackdoc:trackdoc %s' % iDiretorioArquivo) 
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
            iEncontrouProblemas = False
            for Importar in iListaImportacoes:
                iCaminho            = '%s/%s/%s' % (constantes.cntImportacaoFTPPastaRaiz,
                                                    constantes.cntClasseMensagemImportacao,
                                                    str(Importar.pasta_temporaria).encode('utf-8'))
                for (path, dirs,files) in os.walk(iCaminho):
                    for iFile in files:
                        try:
                            iFileLimpo= MultiuploaderImage().limpaNomeImagem(iFile.decode('utf-8'))
                            os.rename(os.path.join(path, iFile), os.path.join(path, iFileLimpo))
                            iCaminho= os.path.join(path, iFileLimpo)
                            iImportarAux= ImportarAuxiliar()
                            iNumero                     = iNumero + 1
                            iImportarAux.numero         = iNumero
                            iImportarAux.caminho        = iCaminho
                            iImportarAux.tamanho        = "%0.1f KB" % (os.path.getsize(iImportarAux.caminho)/(1024.0))
                            iImportarAux.nomeArquivo    = str(os.path.basename(iImportarAux.caminho)).encode('utf-8')
                            iListaAuxiliar.append(iImportarAux)
                        except Exception, e:
                            print 'opa!'
                            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel alimentar a Lista de Importacoes: ' + str(e))
                            iEncontrouProblemas= True
            print iEncontrouProblemas
            return iListaAuxiliar, iEncontrouProblemas
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar obtem Lista Importacoes: ' + str(e))
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
    
    def criaCadastroDeBiometria(self, vUsuario, vIPOrigem, vSalvar=True):
        try:
            iUsuario                    = Usuario().obtemUsuario(vUsuario)
            iCadastro                   = Cadastro_Biometria()
            iCadastro.usuario           = iUsuario
            iCadastro.ip_origem         = vIPOrigem
            iCadastro.pasta_destino     = str(iUsuario.empresa.id_empresa)
            iCadastro.data_importacao   = str(datetime.datetime.today())[:19]
            if vSalvar:
                iCadastro.save()
            return iCadastro
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar cadastro de biometria: ' + str(e))
            return False
    
    def excluiCadastroDeBiometria(self, vUsuario):
        try:
            Cadastro_Biometria.objects.filter(usuario= vUsuario).delete()
            return True
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel excluir cadastro de biometria: ' + str(e))
            return False
    
    def obtemCadastroDeBiometria(self, vUsuario):
        try:
            iListaCadastros= Cadastro_Biometria.objects.filter(usuario= vUsuario)
            if len(iListaCadastros) > 0:
                iCadastro= iListaCadastros[0]
            else:
                iCadastro= None
            return iCadastro
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel verificar existencia de cadastro: ' + str(e))
            return False   