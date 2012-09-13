# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.http                        import HttpResponseRedirect
from django.http                        import HttpResponse

from PyProject_GED                      import oControle, constantes
from PyProject_GED.autenticacao.models  import Usuario, Empresa, Tipo_de_Usuario
from PyProject_GED.relatorios.generators.pdf import PDFGenerator
from PyProject_GED.relatorios.relatorios import ultimosAcessos, estadoUsuarios
from PyProject_GED.historico.models import Log_Usuario

@login_required     
def relatorios(vRequest, vTitulo, vIDVersao=None):
    
    iUsuario= Usuario().obtemUsuario(vRequest.user)
        
    if vRequest.POST:
        try :
            if vRequest.POST.get('tipo_relatorio') == str(constantes.cntTipoRelatorioAcessos):
                return HttpResponseRedirect('/ultimos_acessos/')
            elif vRequest.POST.get('tipo_relatorio') == str(constantes.cntTipoRelatorioUsuario):
                return HttpResponseRedirect('/estado_usuarios/')
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel post relatorios: ' + str(e))
        return False
        
    return render_to_response(
        'relatorios/relatorios.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required     
def estado_usuarios(vRequest, vTitulo):
    try :
        iUsuario        = Usuario().obtemUsuario(vRequest.user)
        iEmpresa        = Empresa().obtemEmpresaPeloID(vRequest.session['IDEmpresa'] )
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(id_tipo_de_usuario= constantes.cntTipoUsuarioSistema)
        iUsuarios       = Usuario.objects.filter(empresa= iEmpresa).filter(tipo_usuario= iTipoUsuario).order_by('id')
        iResposta       = HttpResponse(mimetype='application/pdf')
        iReport         = estadoUsuarios(queryset=iUsuarios)
        iReport.generate_by(PDFGenerator, filename=iResposta)
        Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoRelatorio, iUsuario.id, iEmpresa.id_empresa)
        return iResposta
    
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel post estado_usuarios: ' + str(e))
    return False
        

@login_required     
def ultimos_acessos(vRequest, vTitulo):
    try :
        iUsuario        = Usuario().obtemUsuario(vRequest.user)
        iEmpresa        = Empresa().obtemEmpresaPeloID(vRequest.session['IDEmpresa'] )
        iTipoUsuario    = Tipo_de_Usuario.objects.filter(id_tipo_de_usuario= constantes.cntTipoUsuarioSistema)
        iUsuarios       = Usuario.objects.filter(empresa= iEmpresa).filter(tipo_usuario= iTipoUsuario).order_by('id')
        iResposta       = HttpResponse(mimetype='application/pdf')
        iReport         = ultimosAcessos(queryset=iUsuarios)
        iReport.generate_by(PDFGenerator, filename=iResposta)
        Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoRelatorio, iUsuario.id, iEmpresa.id_empresa)
        return iResposta
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel post ultimos_acessos: ' + str(e))
    return False
        
