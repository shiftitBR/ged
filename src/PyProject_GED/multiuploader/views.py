# -*- coding: utf-8 -*-
from django.shortcuts               import get_object_or_404, render_to_response
from django.conf                    import settings
from django.http                    import HttpResponse, HttpResponseBadRequest
from django.template                import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.utils                   import simplejson
from django.views.decorators.csrf   import csrf_exempt

from models                             import MultiuploaderImage
from documento.forms                    import FormUploadDeArquivo #@UnresolvedImport
from PyProject_GED                      import oControle
from PyProject_GED.indice.models        import Indice_Versao_Valor, Indice
from PyProject_GED.documento.models     import Tipo_de_Documento, Versao, Documento
from PyProject_GED.autenticacao.models  import Usuario
from controle                           import Controle as UploaderControle


import datetime

@csrf_exempt
@login_required 
def multiuploader_delete(request, pk):
    
    if request.method == 'POST':
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.delete()
        return HttpResponse(str(pk))
    else:
        return HttpResponseBadRequest('Only POST accepted')


@login_required 
@csrf_exempt
def multiuploader(vRequest):
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
        iListaTipoDocumento = Tipo_de_Documento().obtemListaTipoDocumento(vRequest.session['IDEmpresa'])
        iListaIndices       = Indice().obtemListaIndices(vRequest.session['IDEmpresa'])
        iTamListaIndices    = len(iListaIndices)
        iListaUsuarios      = Usuario.objects.filter(empresa= iUsuario.empresa.id_empresa)
        iListaNomes         = UploaderControle().obtemListaNomesUsuarios(iListaUsuarios)
        #gerarProtocolo 
        
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get multiuploader: ' + str(e))
            return False
    
    if vRequest.method == 'POST':
        form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
        if form.is_valid():
            try : 
                if vRequest.FILES == None:
                    return HttpResponseBadRequest('Adicione um arquivo')
                #getting file data for farther manipulations
                file = vRequest.FILES[u'files[]']
                wrapped_file = UploadedFile(file)
                filename = wrapped_file.name
                file_size = wrapped_file.file.size
                #salver imagem - tabela multiuploader
                image = MultiuploaderImage()
                image.filename=filename.encode('utf-8')
                image.image=file
                image.key_data = image.key_generate
                image.save(vRequest.session['IDPasta'], vRequest.session['IDEmpresa'])
                result = []
                result.append({"name":filename})
                response_data = simplejson.dumps(result)
                #checking for json data type
                #big thanks to Guy Shapiro
                if "application/json" in vRequest.META['HTTP_ACCEPT_ENCODING']:
                    mimetype = 'application/json'
                else:
                    mimetype = 'text/plain'
            except Exception, e:
                    oControle.getLogger().error('Nao foi possivel fazer upload - multiuploader: ' + str(e))
                    return False
            else:
                try:
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
                    iVersao     = Versao().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                                    1, 1, image.key_data, '1234567')
                    #Salvar Indices
                    for i in range(len(iListaIndices)):
                        iIndice = iListaIndices[i]
                        iValor  = vRequest.POST.get('indice_%s' % iIndice.id_indice)
                        vRequest.POST['indice_%s' % iIndice.id_indice] = ''
                        if iValor != '':
                            Indice_Versao_Valor().salvaValorIndice(iValor, iIndice.id_indice, iVersao.id_versao)
                except Exception, e:
                    oControle.getLogger().error('Nao foi possivel adicionar na tabela documento e versao - multiuploader: ' + str(e))
                    return False
            return HttpResponse(response_data, mimetype=mimetype)    
        else: 
            form = FormUploadDeArquivo(vRequest.POST, iIDEmpresa=vRequest.session['IDEmpresa'])
    else:
        form = FormUploadDeArquivo(iIDEmpresa=vRequest.session['IDEmpresa'])
        
    return render_to_response(
        'documentos/importar_doc.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )
    
@login_required 
def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})