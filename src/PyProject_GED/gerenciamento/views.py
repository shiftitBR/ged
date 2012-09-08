# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.conf                        import settings

from PyProject_GED                      import oControle, constantes
from PyProject_GED.autenticacao.models  import Empresa
from PyProject_GED.documento.models     import Documento, Versao
from objetos_auxiliares                 import GerenciaEmpresa as EmpresaAuxiliar
from controle                           import Controle as GerenciamentoControle


@login_required     
def gerenciamento(vRequest, vTitulo):
    try :
        iTotalDocumentos    = Documento.objects.all().count()
        iTotalVersoes       = Versao.objects.all().count()
        iToalEspacoUtilizado= GerenciamentoControle().obtemEspacoUtilizado(settings.MEDIA_ROOT + '/documentos')
        
        iListaEmpresas      = Empresa.objects.all()
        iListaEmpresasAux   = []
        for iEmpresa in iListaEmpresas :
            iEmpresaAux                 = EmpresaAuxiliar()
            iEmpresaAux.Nome            = iEmpresa.nome
            iEmpresaAux.TotalDocumentos = Documento.objects.filter(empresa= iEmpresa.id_empresa).count()
            iEmpresaAux.TotalVersoes    = Versao.objects.filter(documento__empresa= iEmpresa.id_empresa).count()
            iDiretorioEmpresa           = constantes.cntConfiguracaoDiretorioDocumentos % iEmpresa.id_empresa
            iEmpresaAux.EspacoDisco     = GerenciamentoControle().obtemEspacoUtilizado(iDiretorioEmpresa)
            iEmpresaAux.UsuariosOnLine  = GerenciamentoControle().obtemUsuariosOnLine(iEmpresa.id_empresa)
            iListaEmpresasAux.append(iEmpresaAux)
        
    except Exception, e:
        oControle.getLogger().error('Nao foi possivel get gerenciamento: ' + str(e))
        return False
        
    return render_to_response(
        'gerenciamento/gerenciamento.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
