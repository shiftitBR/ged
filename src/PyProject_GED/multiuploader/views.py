# -*- coding: utf-8 -*-
from django.shortcuts               import get_object_or_404, render_to_response
from django.conf                    import settings
from django.http                    import HttpResponse, HttpResponseBadRequest
from models                         import MultiuploaderImage
from django.core.files.uploadedfile import UploadedFile
#importing json parser to generate jQuery plugin friendly json response
from django.utils                   import simplejson
#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail                 import get_thumbnail
from django.views.decorators.csrf   import csrf_exempt
#ControleDocumento
from documento.controle             import Controle as DocumentoControle #@UnresolvedImport
from PyProject_GED                  import oControle
from documento.forms                import FormUploadDeArquivo #@UnresolvedImport
from indice.controle                import Controle as IndiceControle   #@UnresolvedImport
from django.template                import RequestContext
from django.contrib.auth.decorators import login_required
import logging
log = logging

@csrf_exempt
def multiuploader_delete(request, pk):
    
    if request.method == 'POST':
        log.info('Called delete image. image id='+str(pk))
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
@login_required 
def multiuploader(vRequest):
    
    iUser = vRequest.user
    if iUser:
        iUsuario= DocumentoControle().obtemUsuario(iUser)
    
    iListaTipoDocumento = DocumentoControle().obtemListaTipoDocumento()
    iListaIndices       = DocumentoControle().obtemListaIndices()
    #gerarProtocolo
    
    if vRequest.method == 'POST':
        form = FormUploadDeArquivo(vRequest.POST)
        if form.is_valid():
            try : 
                if vRequest.FILES == None:
                    return HttpResponseBadRequest('Adicione um arquivo')
                #getting file data for farther manipulations
                file = vRequest.FILES[u'files[]']
                wrapped_file = UploadedFile(file)
                filename = wrapped_file.name
                file_size = wrapped_file.file.size
                #writing file manually into model
                #because we don't need form of any type.
                image = MultiuploaderImage()
                image.filename=str(filename)
                image.image=file
                image.key_data = image.key_generate
                image.save()
                log.info('File saving done')
                #Adicionar na tabela versao image.image
                #getting thumbnail url using sorl-thumbnail
                if 'image' in file.content_type.lower():
                    im = get_thumbnail(image, "80x80", quality=50)
                    thumb_url = im.url
                else:
                    thumb_url = ''
                #settings imports
                try:
                    file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
                    file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
                except AttributeError:
                    file_delete_url = 'multi_delete/'
                    file_url = 'multi_image/'+image.key_data+'/'
                #generating json response array
                result = []
                result.append({"name":filename, 
                               "size":file_size, 
                               "url":file_url, 
                               "thumbnail_url":thumb_url,
                               "delete_url":file_delete_url+str(image.pk)+'/', 
                               "delete_type":"POST",})
                response_data = simplejson.dumps(result)
                #checking for json data type
                #big thanks to Guy Shapiro
                if "application/json" in vRequest.META['HTTP_ACCEPT_ENCODING']:
                    mimetype = 'application/json'
                else:
                    mimetype = 'text/plain'
            except:
                form = FormUploadDeArquivo()
            else:
                #Adicionar na tabela documeto e versao
                iAssunto    = vRequest.POST.get('assunto')
                if vRequest.POST.get('eh_publico') != None:
                    iEh_Publico = True
                else:
                    iEh_Publico = False
                iIDTipo_Documento = vRequest.POST.get('tipo_documento')
                iDocumento  = DocumentoControle().salvaDocumento(iIDTipo_Documento, iUsuario, 
                                                oControle.getIDPasta(), iAssunto, iEh_Publico)
                iVersao     = DocumentoControle().salvaVersao(iDocumento.id_documento, iUsuario.id, 
                                                1, 1, image.key_data, '1234567')
                #Salvar Indices
                for i in range(len(iListaIndices)):
                    iIndice = iListaIndices[i]
                    iValor  = vRequest.POST.get('indice_%s' % iIndice.id_indice)
                    vRequest.POST['indice_%s' % iIndice.id_indice] = ''
                    if iValor != '':
                        IndiceControle().salvaValorIndice(iValor, iIndice.id_indice, iVersao.id_versao)
                vRequest.POST['eh_publico'] = False
                vRequest.POST['tipo_documento'] = 0
                vRequest.POST['assunto'] = ''  
                vRequest.POST['usr_responsavel'] = ''
                vRequest.POST['data_validade'] = ''
                vRequest.POST['data_descarte'] = ''
            return HttpResponse(response_data, mimetype=mimetype)    
        else: 
            form = FormUploadDeArquivo(vRequest.POST)
    else:
        form = FormUploadDeArquivo()
        
    return render_to_response(
        'documentos/importar_doc.html',
        locals(),
        context_instance=RequestContext(vRequest),
        )

def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})