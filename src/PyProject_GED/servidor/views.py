# -*- coding: utf-8 -*-

from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.contrib.auth.decorators     import login_required
from django.contrib                     import messages
from django.http                        import HttpResponseRedirect

from PyProject_GED                      import oControle, constantes
from PyProject_GED.autenticacao.models  import Usuario
from PyProject_GED.documento.forms      import FormUploadDeArquivo
from PyProject_GED.seguranca.models     import Pasta
from PyProject_GED.indice.models        import Indice_Pasta, Indice_Versao_Valor
from PyProject_GED.servidor.models      import Importacao_FTP, Servidor
from PyProject_GED.multiuploader.models import MultiuploaderImage
from PyProject_GED.documento.models     import Documento, Versao
from PyProject_GED.qualidade.models     import Norma, Norma_Documento
from PyProject_GED.workflow.models      import Pendencia
from PyProject_GED.historico.models     import Historico, Log_Usuario
from PyProject_GED.ocr.controle         import Controle as ControleOCR
from PyProject_GED.imagem.controle      import Controle as ControleImagem

import datetime
import shutil

@login_required     
def importar_lote(vRequest, vTitulo):
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
        iListaImportar = Importacao_FTP().obtemListaImportacoes(iUsuario)
        if len(iListaImportar) != 0:
            if not Pasta().ehPastaRaiz(vRequest.session['IDPasta'], vRequest.session['IDEmpresa']):
                iListaIndices       = Indice_Pasta().obtemIndicesDaPasta(vRequest.session['IDPasta'])
                iPossuiImportacao = True
            else:
                messages.warning(vRequest, 'Selecione uma Pasta para Inserir Documento!')
        else:
            messages.warning(vRequest, 'Você não possui arquivos aguardando importação.')
        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get importar_lote: ' + str(e))
            return False
    
    if vRequest.POST:
        form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        if form.is_valid():
            try :
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
                iPasta = Pasta().obtemPastaPeloID(vRequest.session['IDPasta'])
                
                for i in range(len(iListaImportar)):
                    iCaminhoPasta = constantes.cntConfiguracaoDiretorioDocumentos%vRequest.session['IDEmpresa'] + "/" + iPasta.diretorio
                    iNomeArquivo_Original= Servidor().copiaArquivo(iListaImportar[i].caminho, iCaminhoPasta)
                    iNomeArquivo= MultiuploaderImage().limpaNomeImagem(iNomeArquivo_Original)
                    if iNomeArquivo == False:
                        raise
                    iImage               = MultiuploaderImage()
                    iImage.filename      = iNomeArquivo
                    iImage.image         = iCaminhoPasta + "/" + iNomeArquivo
                    iImage.key_data      = iImage.key_generate
                    iImage.save(vRequest.session['IDPasta'], vRequest.session['IDEmpresa'])
                    iAssuntoLote= '%s - %02d' % (iAssunto, i+1)
                    iDocumento  = Documento().salvaDocumento(vRequest.session['IDEmpresa'], iIDTipo_Documento, vRequest.session['IDPasta'], 
                                                             iAssuntoLote, iEh_Publico, iResponsavel, iDataValidade, iDataDescarte)
                    iProtocolo  = Documento().gerarProtocolo(iDocumento.id_documento, 1) 
                    iVersao     = Versao().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                                    1, 1, iImage.key_data, iProtocolo)
                    #Associar Normas
                    iNormas = vRequest.POST.getlist('norma')
                    for i in range(len(iNormas)):
                        iNorma = Norma().obtemNorma(iNormas[i])
                        Norma_Documento().criaNorma_Documento(iNorma, iDocumento)
                    #Salvar Indices
                    for i in range(len(iListaIndices)):
                        iIndice = iListaIndices[i]
                        iValor  = vRequest.POST.get('indice_%s' % iIndice.id_indice)
                        if iValor != '':
                            Indice_Versao_Valor().salvaValorIndice(iValor, iIndice.id_indice, iVersao.id_versao)
                    try:
                        ControleOCR().executaOCR(iVersao)
                        ControleImagem().comprimeImagem(iVersao)
                    finally:
                        Pendencia().criaPendenciasDoWorkflow(iDocumento)
                        Historico().salvaHistorico(iVersao.id_versao, constantes.cntEventoHistoricoImportar, 
                                                   iUsuario.id, vRequest.session['IDEmpresa'])
                        Log_Usuario().salvalogUsuario(constantes.cntEventoHistoricoImportar, iUsuario.id, 
                                                  vRequest.session['IDEmpresa'], vIDVersao=iVersao.id_versao)
                return HttpResponseRedirect('/sucesso/' + str(constantes.cntFuncaoImportar) + '/')
            except Exception, e:
                oControle.getLogger().error('Nao foi possivel get importar_lote: ' + str(e))
                messages.warning(vRequest, 'Não foi possível importar os arquivos solicitados!')
                return HttpResponseRedirect('/importar_lote/')
        else:
            form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
    else: 
        form = FormUploadDeArquivo(iIDEmpresa=vRequest.session['IDEmpresa'])
    return render_to_response(
        'importar/importar_lote.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    