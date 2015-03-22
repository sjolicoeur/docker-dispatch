# Dispatch
# runs on the exposed nodes 
# reads the registered images and adds them to the HAProxy config
from marathon import MarathonClient
import os
from urlparse import urlparse
import time
import logging
from jinja2 import Environment, FileSystemLoader
import subprocess
import jinja2
import re
log = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)

# ENV VARS
MARATHON_HOST = os.getenv("MARATHON_HOSTS", "http://localhost:8080")
MESOS_HOST = os.getenv("MESOS_HOSTS", "http://localhost:5050")
LOCAL_IP = os.getenv("LOCAL_IP", "localhost")
BASE_DOMAIN=os.getenv('DISPATCH_BASE_DOMAIN','heartlabs.co')
HA_PASSWORD=os.getenv('HA_PASSWORD', 'catn1pp3rZ')

###
c = MarathonClient(MARATHON_HOST)
# or multiple servers:
# c = MarathonClient(['http://host1:8080', 'http://host2:8080'])

HAPROXY_RESTART_CMD = [
        '/usr/sbin/haproxy '
        '-f /etc/haproxy/haproxy.cfg '
        '-p /var/run/haproxy.pid '
        '-sf $(cat /var/run/haproxy.pid)'
    ]
# /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)

env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))



get_docker_host = lambda: urlparse(os.getenv('DOCKER_HOST')).hostname


def read_from_marathon():
    """
    # www -> normal web
    # wwwp -> password protected
    # wwws -> ssl
    """
    apps = {
        "mesos" : {
            "config":[{"ip" : LOCAL_IP, "port": 5050 }],
            "app_type": "wwwp"
            },
        "marathon" : {
            "config":[{"ip" : LOCAL_IP, "port": 8080}],            
            "app_type": "wwwp"
        },
        "hap": {
            "config":[{"ip" : LOCAL_IP, "port": 9090}],            
            "app_type": "wwwp"
        },
        "ha_admin": {
            "config":[{"ip" : LOCAL_IP, "port": 8181}],            
            "app_type": "wwwp"
        },
        "registry": {
            "config":[{"ip" : LOCAL_IP, "port": 5959}],            
            "app_type": "www"

        },        
        "jenkins": {
            "config":[{"ip": "172.30.1.43", "port": 8080}],
            "app_type": "www"
        },
    }
    app_regex = r'^/(?P<app_name>[a-zA-Z0-9|\-|\.]+)\.(?P<app_type>(www)|(wwwp)|(wwws))$'
    for task in  c.list_tasks():
        app_id = task.app_id
        rule_match = re.match(app_regex, app_id)
        if rule_match:
            app_info = rule_match.groupdict() # {'app_name': 'de-a.sfsfds.mo', 'app_type': 'wwws'}
            app_name = app_info['app_name']
            app_type = app_info['app_type']
        else:
            app_name = app_id.replace("/", "")
            app_type = 'www'
        port = task.ports[0]
        ip = task.host
        if app_name not in apps:
            apps[app_name] = {
                "app_type": app_type,
                "config":[]
            }
        apps[app_name]["config"].append({"ip":ip, "port": port})
    return apps

def generate_config(apps):
    template = env.get_template('ha_proxy.conf.jinja2')
    content = template.render(
            apps=apps,
            base_domain=BASE_DOMAIN,
            password=HA_PASSWORD
        )
    return content

def compare_to_current_config(compare_to):
    config_file = ''
    with open('/etc/haproxy/haproxy.cfg', 'r') as f:
        config_file = f.read()
    return config_file == compare_to

def register_apps():
    apps = read_from_marathon()
    content = generate_config(apps)
    config_is_identical = compare_to_current_config(content)
    if not config_is_identical:
        with open('/etc/haproxy/haproxy.cfg', 'w') as f:
            f.write(content)
        subprocess.Popen(HAPROXY_RESTART_CMD, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)


if __name__ == '__main__':
    flag = True
    log.info("Looking to register apps to HAProxy")
    register_apps()
