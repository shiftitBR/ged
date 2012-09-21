# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.contrib                     import messages
from django.http                        import HttpResponse

from PyProject_GED                      import oControle, constantes
from PyProject_GED.seguranca.models     import Funcao_Grupo
from PyProject_GED.autenticacao.models  import Usuario, Empresa
from PyProject_GED.imagem.controle      import Controle as ImagemControle
from PyProject_GED.historico.models     import Log_Usuario, Historico

import os

@login_required     
def tipo_exportar(vRequest, vTitulo, vIDVersao=None):
    
    iUsuario        = Usuario().obtemUsuario(vRequest.user)
    if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoExportar):
        iPossuiPermissao= True
    else:
        messages.warning(vRequest, 'Você não possui permissão para executar esta função.') 
        
    if vRequest.POST:
        try :
            iArquivo    = ImagemControle().converteExtencaoImagem(vIDVersao, int(vRequest.POST.get('tipo_exportar')))
            iFile       = open(iArquivo,"r")
            response    = HttpResponse(iFile.read())
            response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iArquivo)[1]
            return response
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post relatorios: ' + str(e))
            return False
        finally:
            Historico().salvaHistorico(vIDVersao, constantes.cntEventoHistoricoExportar, 
                                          iUsuario.id, vRequest.session['IDEmpresa'])
            Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoExportar, 
                                          iUsuario.id, vRequest.session['IDEmpresa'])
            ImagemControle().deletaImagemTemporaria(iArquivo)
        
    return render_to_response(
        'exportar/tipo_exportar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
        