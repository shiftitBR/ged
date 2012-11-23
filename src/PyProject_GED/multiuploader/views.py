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
from PyProject_GED.multiuploader.models import Downloader
import Queue

oListaUploads= {}
iConexoesSimultaneas = 1
iSemafaroGeral = BoundedSemaphore(value=iConexoesSimultaneas)

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
            #iSemafaroGeral.acquire()
            if vRequest.FILES == None:
                return HttpResponseBadRequest('Adicione um arquivo')
            file = vRequest.FILES[u'files[]'.encode('utf-8')]
            wrapped_file = UploadedFile(file)
            filename = wrapped_file.name
            file_size = wrapped_file.file.size
            #salvar imagem - tabela multiuploader
            image               = MultiuploaderImage()
            image.filename      = filename
            image.image         = file
            image.key_data      = image.key_generate
            image.save(vRequest.session['IDPasta'], vRequest.session['IDEmpresa'])
            result = []
            result.append({"name":filename})
            response_data = simplejson.dumps(result)
            if "application/json" in vRequest.META['HTTP_ACCEPT_ENCODING']:
                mimetype = 'application/json'
            else:
                mimetype = 'text/plain'
            #iSemaforo = MultiuploaderImage().obtemSemaforo(vRequest.user.id)
            #iSemaforo.acquire()
            
            
            queue = Queue.Queue()
            # create a thread pool and give them a queue
            t = Downloader(queue)
            t.setDaemon(True)
            t.start()
         
            # give the queue some data
            queue.put((vRequest.session, image.id))
         
            # wait for the queue to finish
            queue.join()
            
            
            #vRequest.session['Images'].append(image.id)
            #vRequest.session.modified = True
            #iSemaforo.release()
            #iSemafaroGeral.release()
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