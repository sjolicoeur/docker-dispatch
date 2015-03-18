from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Token(models.Model):
    owner = models.ForeignKey(User)
    token = models.SlugField(unique=True)
    
# class DockerImageDeployJob(models.Model):
#     DEPLOY_HTTPS = 'wwws'
#     DEPLOY_HTTP = 'www'
#     DEPLOY_PASS = 'wwwp'
#     DEPLOY_TYPES = (
#             (DEPLOY_HTTP, 'HTTP service'),
#             (DEPLOY_HTTPS, 'HTTPS service'),
#             (DEPLOY_PASS, 'Password Protect'),
#         )
#     title = models.CharField(max_length=90)
#     image_name = models.CharField(max_length=90)
#     type = models.CharField(max_length=5, choices=DEPLOY_TYPES, default=DEPLOY_HTTP)
#     tag_name = models.CharField(max_length=30, default="latest")
#     cpu = models.FloatField(default=0.1) # max it at 2 in settings
#     memory = models.FloatField(default=16) # max it at 500 in settings
#     instances = models.IntegerField()
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)

# class ExposedPort(models.Model):
#     docker_image = models.ForeignKey(DockerImageDeployJob)
#     port = models.IntegerField()

# class EnvVariables(models.Model):
#     docker_image = models.ForeignKey(DockerImageDeployJob)
#     name = models.CharField(max_length=20)
#     value = models.CharField(max_length=35)

# ====

# ubuntu@172:~$ cat cpywww.json 
# {
#   "container": {
#     "type": "DOCKER",
#     "docker": {
#       "image": "sjolicoeur/hello-word2:prot",
#       "network": "BRIDGE",
#       "portMappings": [
#         { "containerPort": 8080, "hostPort": 0, "protocol": "tcp" }
#       ]
#     }
#   },
#   "id": "ccpy.www",
#   "instances": 1,
#   "cpus": 0.2,
#   "mem": 50,
#   "ports":[8080],
#   "env": {
#     "SAY": "tomy_little_friends"
#   }
# }
# ubuntu@172:~$ http -v PUT http://localhost:8080/v2/apps/demo?force=true @cpywww.json
