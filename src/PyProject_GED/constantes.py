'''
Created on Jul 11, 2012

@author: Shift IT | www.shiftit.com.br
'''
from django.conf    import settings


#Configuracoes
cntConfiguracaoDiretorioDocumentos= settings.MEDIA_ROOT + '/documentos/empresa_%03d'
cntConfiguracaoPastaDocumentos= 'documentos'

#Servicos
cntServicosCriaPastas= 1
cntServicosAtualizaEmpresa= 2
cntServicosCriaTipoUsuario= 3
cntServicosCriaTipoDeIndice= 4
cntServicosCriaTipodeDocumento= 5