# Todo
install haproxy
install supervisord
make small webserver that will read from ETCD and write the HAPROXY cfg file.
jinja?
send cmd to reboot the haproxy if there is a change
add health checks

# other project, simple webservice to receive notifications from CI env and create fleet files  and execute the cmd
# should have a white list of repos
# accept API keys to connect
# show an interface of the running images taken from etcd and  doing some form of polling
# setup a DB for the provisioned env 
# use and execute fab files?

# docker dynamic ports `-p :9200 -p :9300`
# how to get the dockerhost?? or private ip of the machine?
# 
