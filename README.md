# Todo
 - [x] install haproxy
 - [x] install supervisord
make small webserver that will read from ETCD and write the HAPROXY cfg file.
 - [x] jinja? yes
 - [x] send cmd to reboot the haproxy if there is a change
 - [x] add health checks

 - [] other project, simple webservice to receive notifications from CI env and create fleet files  and execute the cmd
 - [] should have a white list of repos
 - [] accept API keys to connect
 - [ sorta done with the haproxy list? need another ] show an interface of the running images taken from etcd and  doing some form of polling
 - [] setup a DB for the provisioned env 
 - [] use and execute fab files?

 - [x] docker dynamic ports `-p :9200 -p :9300`
 - [] how to get the dockerhost?? or private ip of the machine?

