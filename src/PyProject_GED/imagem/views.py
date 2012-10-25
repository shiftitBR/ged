# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.contrib                     import messages
from django.http                        import HttpResponse

from PyProject_GED                      import oControle, constantes
from PyProject_GED.seguranca.models     import Funcao_Grupo
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.imagem.controle      import Controle as ImagemControle
from PyProject_GED.historico.models     import Log_Usuario, Historico
from django.conf                        import settings

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
            iArquivo    = ImagemControle().converteExtencaoImagem(vIDVersao, int(vRequest.POST.get('tipo_exportar')), iUsuario.id)
            iFile       = open(iArquivo,"r")
            response    = HttpResponse(iFile.read())
            response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(iArquivo)[1]
            return response
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel exportar a imagem: ' + str(e))
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
    
@login_required     
def negativar_imagem(vRequest, vTitulo):
    iHtml       = []      
    try :
        iDiretorioImagemTemporaria= vRequest.session['Imagem_Temporaria']
        iDiretorioRoot= settings.PROJECT_ROOT_PATH
        iDiretorioMediaImagemTemproaria= iDiretorioImagemTemporaria[len(iDiretorioRoot):]
        ImagemControle().negativaImagem(iDiretorioImagemTemporaria)
        iHtml.append(iDiretorioMediaImagemTemproaria)
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel negativar a imagem: ' + str(e))
        return False
        
    return HttpResponse(''.join(iHtml))

@login_required     
def rotacionar_imagem(vRequest, vTitulo, vLado):
    iHtml       = []      
    try :
        iDiretorioImagemTemporaria= vRequest.session['Imagem_Temporaria']
        iDiretorioRoot= settings.PROJECT_ROOT_PATH
        iDiretorioMediaImagemTemproaria= iDiretorioImagemTemporaria[len(iDiretorioRoot):]
        ImagemControle().rotacionaImagem(iDiretorioImagemTemporaria, vLado)
        iHtml.append(iDiretorioMediaImagemTemproaria)
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel rotacionar a imagem: ' + str(e))
        return False
        
    return HttpResponse(''.join(iHtml))
