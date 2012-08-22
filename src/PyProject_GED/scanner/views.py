# -*- coding: utf-8 -*-
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.contrib                     import messages

from PyProject_GED.documento.forms      import FormUploadDeArquivo
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.seguranca.models     import Funcao_Grupo
from PyProject_GED.documento.models     import Tipo_de_Documento, Documento, Versao
from PyProject_GED.indice.models        import Indice, Indice_Versao_Valor
from PyProject_GED.scanner.controle     import Controle as ControleScanner
from PyProject_GED.ocr.controle         import Controle as ControleOCR
from PyProject_GED.documento.controle   import Controle as DocumentoControle
from PyProject_GED                      import oControle

import datetime
import constantes #@UnresolvedImport

@login_required     
def importar(vRequest, vTitulo):
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
            
        if Funcao_Grupo().possuiAcessoFuncao(iUsuario, constantes.cntFuncaoImportar):
            iListaTipoDocumento = Tipo_de_Documento().obtemListaTipoDocumentoDaEmpresa(vRequest.session['IDEmpresa'])
            iListaIndices       = Indice().obtemListaIndices(vRequest.session['IDEmpresa'])
            iTamListaIndices    = len(iListaIndices)
            iListaUsuarios      = Usuario.objects.filter(empresa= iUsuario.empresa.id_empresa)
            iListaNomes         = DocumentoControle().obtemListaNomesUsuarios(iListaUsuarios)
            iPossuiPermissao    = True
        else:
            messages.warning(vRequest, 'Você não possui permissão para executar esta função.')
        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get importar: ' + str(e))
            return False
    
    if vRequest.POST:
        form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        if form.is_valid():
            try:
                if ControleScanner().executaScanner():
                    iImage= vRequest.session['Image'] # Verificar
                    #Adicionar na tabela documeto e versao
                    if len(vRequest.POST.get('data_validade')) != 10:
                        iDataValidade= datetime.datetime.now()
                    else:
                        iListaDataValidade= vRequest.POST.get('data_validade').split('/')
                        iDataValidade= datetime.datetime(int(iListaDataValidade[2]), int(iListaDataValidade[1]), int(iListaDataValidade[0]), 00, 00, 00)
                    if len(vRequest.POST.get('data_descarte')) != 10:
                        iDataDescarte= datetime.datetime.now()
                    else:
                        iListaDataDescarte= vRequest.POST.get('data_descarte').split('/')
                        iDataDescarte= datetime.datetime(int(iListaDataDescarte[2]), int(iListaDataDescarte[1]), int(iListaDataDescarte[0]), 00, 00, 00)
                    iAssunto    = vRequest.POST.get('assunto')
                    iIDResponsavel= vRequest.POST.get('usr_responsavel')
                    iResponsavel= Usuario().obtemUsuarioPeloID(iIDResponsavel)
                    if vRequest.POST.get('eh_publico') != None:
                        iEh_Publico = True
                    else:
                        iEh_Publico = False
                    iIDTipo_Documento = vRequest.POST.get('tipo_documento')
                    iDocumento  = Documento().salvaDocumento(vRequest.session['IDEmpresa'], iIDTipo_Documento, vRequest.session['IDPasta'], 
                                                             iAssunto, iEh_Publico, iResponsavel, iDataValidade, iDataDescarte)
                    iProtocolo  = Documento().gerarProtocolo(iDocumento.id_documento, 1) 
                    iVersao     = Versao().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                                    1, 1, iImage.key_data, iProtocolo)
                    #Salvar Indices
                    for i in range(len(iListaIndices)):
                        iIndice = iListaIndices[i]
                        iValor  = vRequest.POST.get('indice_%s' % iIndice.id_indice)
                        if iValor != '':
                            Indice_Versao_Valor().salvaValorIndice(iValor, iIndice.id_indice, iVersao.id_versao)
                    ControleOCR().executaOCR(iVersao)
                else:
                    messages.warning(vRequest, 'Não foi possível digitalizar imagem!')
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel importar: ' + str(e))
                return False
        else:
            form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
    else: 
        form = FormUploadDeArquivo(iIDEmpresa=vRequest.session['IDEmpresa'])
                                           
    return render_to_response(
        'scanner/importar.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )