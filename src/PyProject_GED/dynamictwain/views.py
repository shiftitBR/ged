import json, re
from django.shortcuts import render_to_response as render
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import resolve

from PyProject_GED.dynamictwain.models import TempFormData




@csrf_exempt
def upload(request):
    print '>>>>>>>>>>>>>>>>>>>>>> upload view'
    if not request.method == 'POST':
        pass # gofuckyourself
    
    # RemoteFile
    f = request.FILES['RemoteFile']
    print type(f)
    print f

    # Extract the ID.
    uid = re.match('.*\[(.+)\].*', f.name).group(1)
    print uid
    real_filename = f.name.replace("[%s]" % uid, '')
    print real_filename

    # Grab the temp data
    tmp = TempFormData.objects.get(pk=uid)
    print tmp
    tmp.scan = f
    tmp.save()
    print 'saveeee'
    
    return HttpResponse(True)


@csrf_exempt
def form(request):
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>> form'
    # Convert to JSON for storage
    get = json.dumps(request.GET)
    print get
    post = json.dumps(request.POST)
    print post
    # Create a temporary object for storing request data
    print request.GET['orig']
    tmp = TempFormData(orig_url=request.GET['orig'],json_get=get, json_post=post)
    print tmp
    tmp.save()
    print '>>>>>>>>>>>>>> salvouo'
    uid = tmp.pk
    print uid
    response = json.dumps({'uid':uid})
    print response

    return HttpResponse(response, mimetype='application/json')


@csrf_exempt
def redirect(request):
    print '>>>>>>>>>>>>>>>redirect'
    uid = request.GET['uid']
    data = TempFormData.objects.get(pk=uid)
    print data


    # We create a brand new request that we route internally to the
    # developer's view.

    # It is quite messy because Django requests are (supposed to be)
    # immutable

    new_request = request
    
    post = new_request.POST.copy()
    post.update(json.loads(data.json_post))
    new_request.POST = post
    
    get = new_request.GET.copy()
    get.update(json.loads(data.json_get))
    new_request.GET = get

    files = new_request.FILES.copy()
    print files
    files['pdf'] = data.scan
    new_request._files = files


    final_view = resolve(data.orig_url)[0]
    return final_view(new_request)

def foo(request):
    print '<<<<<<<<<<<<<<<<<<<<<<<<'
    val = request.GET['some_name']
    print val
    f = request.FILES
    print f
    return HttpResponse('Received value: %s. With file: %s' % (val,f))
