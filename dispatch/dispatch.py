# Dispatch
# runs on the exposed nodes 
# reads the registered images and adds them to the HAProxy config

from docker import Client
from docker.utils import kwargs_from_env
import os
from urlparse import urlparse
import etcd
import time
import logging
from jinja2 import Environment, FileSystemLoader

import jinja2

log = logging.getLogger(__name__)
ROOT_KEY = os.getenv('QUARTERMASTER_ROOT_KEY','/ha_quartermaster')

BASE_DIR = os.path.dirname(__file__)

# TEMPLATE_FILE = "templates/ha_proxy.conf.jinja2"

env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))

# template = env.get_template('ha_proxy.conf.jinja2')
# print template.render(hello='variables', go='here')


# env = kwargs_from_env(assert_hostname=False)
# env['version'] = os.getenv('DOCKER_API_VERSION', '1.15')
# client = Client(**env)

get_docker_host = lambda: urlparse(os.getenv('DOCKER_HOST')).hostname


def read_from_etcd():
    etcd_client = etcd.Client(host=get_docker_host())
    keys = etcd_client.read(ROOT_KEY, recursive=True)
    apps = {}
    for key in keys.children:
        print key, dir(key), key.key, key.value
        _, _, app_name, ip, port = key.key.split("/")
        app_type = key.value
        if app_name not in apps:
            apps[app_name] = []
        # if app_type.lower() in ["www"]:
        apps[app_name].append({"ip":ip, "port": port, "app_type": app_type})
    return apps

def register_apps():
    apps = read_from_etcd()
    template = env.get_template('ha_proxy.conf.jinja2')
    content = template.render(apps=apps, base_domain=os.getenv('DISPATCH_BASE_DOMAIN','example.com'))
    # check if content differs from current haproxy config 
    # if it does write and reload haproxy
    # if not do nothing


if __name__ == '__main__':
    flag = True
    while(flag):
        log.info("Looking to register apps to HAProxy")
        register_apps()
        time.sleep(60*5)
