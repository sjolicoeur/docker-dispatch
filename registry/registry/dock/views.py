from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from registry.dock.models import Token
from django.contrib.auth.decorators import login_required
import simplejson
from django.http import HttpResponse, HttpResponseNotFound
from registry.dock.validator import DockValidator
import os 
import json
import requests
import logging

log = logging.getLogger(__name__)
BASE_DOMAIN=os.getenv('DISPATCH_BASE_DOMAIN','heartlabs.co')


def valid_token(request):
    print request.META.keys()
    user_token = request.META.get('HTTP_X_API_AUTH_CREDENTIALS', '')
    token = Token.objects.filter(token=user_token).exists()
    return token

def send_job(job_info):
    data_packet =  {
        "container": {
            "type": "DOCKER",
            "docker": {
                "image": "%s:%s" % (
                        job_info['image_name'],job_info['tag_name']),
                "network": "BRIDGE",
                "portMappings": [
                    { "containerPort": job_info['port'], "hostPort": 0, "protocol": "tcp" }
                ]
            }
        },
        "id": "%s.%s" % (job_info['title'], job_info['type']),
        "instances": job_info['instances'],
        "cpus": job_info['cpu'],
        "mem": job_info['memory'],
        "ports":[job_info['port']],
        "env": {},
        "uris": [ "file:///home/ubuntu/.dockercfg" ],
    }

    for name, value in job_info['env_vars']:
        data_packet['env'][name] = value

    url = 'http://localhost:8080/v2/apps/?force=true'
    try:
        log.warn(data_packet)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data_packet))
        if r.ok:
            return True, "success!"
        return False, "Failed status: %s" % str(r.status_code)
    except requests.ConnectionError:
        return False, "Failed to connect"
# ubuntu@172:~$ http -v PUT http://localhost:8080/v2/apps/demo?force=true @cpywww.json


# @login_required
@csrf_exempt
def home(request):
    if request.user.is_authenticated() or valid_token(request):
        if request.method == "POST":
        
            data = simplejson.loads(request.POST.get('json'))
            print data
            validator = DockValidator(data)

            if validator.is_valid():
                domain = "%s.%s" % (
                                validator.clean_data['title'],
                                BASE_DOMAIN
                            )
                if "env" in data:
                    for val in data["env"]:
                        if "name" in val and val["name"] == "domain":
                            domain = val["value"]
                
                result = {
                    "data": {
                        "url": domain,
                        "img_string": "%s:%s" % (
                                validator.clean_data['image_name'],
                                validator.clean_data['tag_name'],
                            ),
                        "service_type": validator.clean_data['type']
                        },
                    "status": "ok"
                }
                success, msg = send_job(validator.clean_data)
                if success:
                    return HttpResponse(
                            simplejson.dumps(result), 
                            content_type="application/json")
                else:
                    return HttpResponse(
                            simplejson.dumps({
                                "status": "error",
                                "errors": [msg]
                            }), 
                            content_type="application/json")
            else:
                print validator.errors
                result = {
                    "errors": validator.errors,
                    "status": "error"
                }
                return HttpResponse(
                        simplejson.dumps(result), 
                        content_type="application/json")
        return render(
            request,
            'dock/dockerimagedeployjob_form.html',
            {
                'num_env': [i for  i in range(5)]
            }
        )
    else:
        print "is ajax?",request.is_ajax()
        return HttpResponse("SIGH!")
    



# list current jobs and their url
# have button to  add new job on submit refresh page
# curl -XGET -H "X-Requested-With: XMLHttpRequest" \
#    -H 'X-API-AUTH-CREDENTIALS:test' http://127.0.0.1:8000/ 




