# -*- coding: utf-8 -*-
from django.shortcuts               import get_object_or_404, render_to_response
from django.conf                    import settings
from django.http                    import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.utils                   import simplejson
from django.views.decorators.csrf   import csrf_exempt

from models                         import MultiuploaderImage
from PyProject_GED                  import oControle
from threading import BoundedSemaphore
import Queue
from PyProject_GED.autenticacao.models import Usuario
import re

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
    #vRequest.session['Images'] = False
    
    if vRequest.method == 'POST':
        try:
            if vRequest.FILES == None:
                return HttpResponseBadRequest('Adicione um arquivo')
            file = vRequest.FILES[u'files[]'.encode('utf-8')]
            file.name= MultiuploaderImage().limpaNomeImagem(file.name)
            wrapped_file = UploadedFile(file)
            filename = wrapped_file.name
            file_size = wrapped_file.file.size
            #salvar imagem - tabela multiuploader
            image               = MultiuploaderImage()
            image.filename      = image.limpaNomeImagem(filename)
            image.image         = file
            image.key_data      = image.key_generate
            image.usuario       = Usuario().obtemUsuario(vRequest.user)
            image.grupo         = vRequest.session['IDGrupo_Upload']
            image.save(vRequest.session['IDPasta'], vRequest.session['IDEmpresa'])
            result = []
            result.append({"name":filename})
            response_data = simplejson.dumps(result)
            if "application/json" in vRequest.META['HTTP_ACCEPT_ENCODING']:
                mimetype = 'application/json'
            else:
                mimetype = 'text/plain'
            return HttpResponse(response_data, mimetype=mimetype)
        except Exception, e:
                oControle.getLogger().error('Nao foi possivel fazer upload - multiuploader: ' + str(e))
                vRequest.session['Images']= False
                return False
                
@login_required 
def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})