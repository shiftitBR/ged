# -*- coding: utf-8 -*-
from django.shortcuts               import get_object_or_404, render_to_response
from django.conf                    import settings
from django.http                    import HttpResponse, HttpResponseBadRequest
from django.template                import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.utils                   import simplejson
from django.views.decorators.csrf   import csrf_exempt

from sorl.thumbnail                     import get_thumbnail
from models                             import MultiuploaderImage
from documento.forms                    import FormUploadDeArquivo #@UnresolvedImport
from PyProject_GED                      import oControle
from PyProject_GED.indice.models        import Indice_Versao_Valor, Indice
from PyProject_GED.documento.models     import Tipo_de_Documento, Versao, Documento
from PyProject_GED.autenticacao.models  import Usuario

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

@csrf_exempt
@login_required 
def multiuploader(vRequest):
    try :
        iUser = vRequest.user
        if iUser:
            iUsuario= Usuario().obtemUsuario(iUser)
        iListaTipoDocumento = Tipo_de_Documento().obtemListaTipoDocumento(vRequest.session['IDEmpresa'])
        iListaIndices       = Indice().obtemListaIndices(vRequest.session['IDEmpresa'])
        iTamListaIndices    = len(iListaIndices)
        iListaUsuarios      = Usuario.objects.filter(empresa= iUsuario.empresa.id_empresa)
        iListaNomes         = []
        iListaNomesUsuarios = ''
        for i in range (len(iListaUsuarios)):
            iNome = iListaUsuarios[i].first_name + ' ' + iListaUsuarios[i].last_name
            iListaNomes.append("teste_%d" %i)
            iListaNomesUsuarios = '"'+iNome + '",'+ iListaNomesUsuarios
        iListaNomesUsuarios = "[&quot;Alabama&quot;,&quot;Alaska&quot;,&quot;Arizona&quot;,&quot;Arkansas&quot;,&quot;California&quot;,&quot;Colorado&quot;,&quot;Connecticut&quot;,&quot;Delaware&quot;,&quot;Florida&quot;,&quot;Georgia&quot;,&quot;Hawaii&quot;,&quot;Idaho&quot;,&quot;Illinois&quot;,&quot;Indiana&quot;,&quot;Iowa&quot;,&quot;Kansas&quot;,&quot;Kentucky&quot;,&quot;Louisiana&quot;,&quot;Maine&quot;,&quot;Maryland&quot;,&quot;Massachusetts&quot;,&quot;Michigan&quot;,&quot;Minnesota&quot;,&quot;Mississippi&quot;,&quot;Missouri&quot;,&quot;Montana&quot;,&quot;Nebraska&quot;,&quot;Nevada&quot;,&quot;New Hampshire&quot;,&quot;New Jersey&quot;,&quot;New Mexico&quot;,&quot;New York&quot;,&quot;North Dakota&quot;,&quot;North Carolina&quot;,&quot;Ohio&quot;,&quot;Oklahoma&quot;,&quot;Oregon&quot;,&quot;Pennsylvania&quot;,&quot;Rhode Island&quot;,&quot;South Carolina&quot;,&quot;South Dakota&quot;,&quot;Tennessee&quot;,&quot;Texas&quot;,&quot;Utah&quot;,&quot;Vermont&quot;,&quot;Virginia&quot;,&quot;Washington&quot;,&quot;West Virginia&quot;,&quot;Wisconsin&quot;,&quot;Wyoming&quot;]"
        print '>>>>>>>>>>>>>>>>'
        print iListaNomesUsuarios
        print str(iListaNomes)
        #gerarProtocolo 
    except Exception, e:
            oControle.getLogger().error('Nao foi possivel get multiuploader: ' + str(e))
            return False
    
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
                #writing file manually into  odel
                #because we don't need form of any type.
                image = MultiuploaderImage()
                image.filename=str(filename)
                image.image=file
                image.key_data = image.key_generate
                image.save(vRequest.session['IDPasta'])
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
            except Exception, e:
                    oControle.getLogger().error('Nao foi possivel fazer upload - multiuploader: ' + str(e))
                    return False
            else:
                try:
                    #Adicionar na tabela documeto e versao
                    iListaDataValidade= vRequest.POST.get('data_validade').split('/')
                    iDataValidade= datetime.datetime(int(iListaDataValidade[2]), int(iListaDataValidade[1]), int(iListaDataValidade[0]), 00, 00, 00)
                    iListaDataDescarte= vRequest.POST.get('data_descarte').split('/')
                    iDataDescarte= datetime.datetime(int(iListaDataDescarte[2]), int(iListaDataDescarte[1]), int(iListaDataDescarte[0]), 00, 00, 00)
                    iAssunto    = vRequest.POST.get('assunto')
                    if vRequest.POST.get('eh_publico') != None:
                        iEh_Publico = True
                    else:
                        iEh_Publico = False
                    iIDTipo_Documento = vRequest.POST.get('tipo_documento')
                    iDocumento  = Documento().salvaDocumento(vRequest.session['IDEmpresa'], iIDTipo_Documento, iUsuario, 
                                                    vRequest.session['IDPasta'], iAssunto, iEh_Publico, iDataValidade, iDataDescarte)
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
            form = FormUploadDeArquivo(vRequest.POST)
    else:
        form = FormUploadDeArquivo()
        
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