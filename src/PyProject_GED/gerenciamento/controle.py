# -*- coding: utf-8 -*- 

import logging
import datetime
from PyProject_GED.autenticacao.models import Usuario
import os

class Controle(object):
    
    oLogger= logging.getLogger('PyProject_GED.controle')
    
    def setLogger(self, vLogger):
        self.oLogger= vLogger
    
    def getLogger(self):
        return self.oLogger
    
    def obtemUsuariosOnLine(self, vIDEmpresa):
        try:
            #Usuarios logados durante a ultima hora
            iTempo          = datetime.datetime.now() - datetime.timedelta(hours=1)
            iTempoSQL       = datetime.datetime.strftime(iTempo, '%Y-%m-%d %H:%M:%S')
            iUsuarios       = Usuario.objects.filter(last_login__gt=iTempoSQL,
                                        is_active__exact=1).filter(empresa= vIDEmpresa).order_by('-last_login')
            return iUsuarios
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtem Usuarios OnLine: ' + str(e))
            return False
        
    def obtemEspacoUtilizado(self, vCaminhoPasta):
        try:
            iEspacoUtilizado = 0
            for (path, dirs, files) in os.walk(vCaminhoPasta):
                for iFile in files:
                    iFilename = os.path.join(path, iFile)
                    iEspacoUtilizado += os.path.getsize(iFilename)
            iEspaco =  "%0.1f MB" % (iEspacoUtilizado/(1024*1024.0))
            return iEspaco
        except Exception, e:
            self.getLogger().error('Nao foi possivel obtem Espaco Utilizado: ' + str(e))
            return False
