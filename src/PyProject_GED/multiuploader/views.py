# -*- coding: utf-8 -*-
from django.shortcuts               import get_object_or_404, render_to_response
from django.conf                    import settings
from django.http                    import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.utils                   import simplejson
from django.views.decorators.csrf   import csrf_exempt

from models                             import MultiuploaderImage
from PyProject_GED                      import oControle

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
    if vRequest.method == 'POST':
        try:
            if vRequest.FILES == None:
                return HttpResponseBadRequest('Adicione um arquivo')
            file = vRequest.FILES[u'files[]']
            wrapped_file = UploadedFile(file)
            filename = wrapped_file.name
            file_size = wrapped_file.file.size
            #salvar imagem - tabela multiuploader
            print '>>>>>>>>>>>>>>>'
            iFileName= MultiuploaderImage().limpaNomeImagem(filename.encode('utf-8'))
            print iFileName
            image               = MultiuploaderImage()
            image.filename      = iFileName
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
            try:
                if vRequest.session['Images'] == False:
                    iListaImages = '%s' % image.id
                    vRequest.session['Images'] = iListaImages
                else:
                    iListaImages = '%s , %s' % (vRequest.session['Images'], image.id)
                    vRequest.session['Images'] = iListaImages
            except:
                iListaImages = '%s' % image.id
                vRequest.session['Images'] = iListaImages
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