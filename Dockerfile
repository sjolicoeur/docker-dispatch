FROM    ubuntu:14.04

MAINTAINER Stephane Jolicoeur <s.jolicoeur+docker@gmail.com>

RUN     apt-get update && apt-get install -y apt-utils && apt-get install -y  \
            python-setuptools \
            build-essential \
            autoconf \
            libtool \
            python-dev \
            libffi-dev \
            libssl-dev \
            python-openssl \
            haproxy \
            &&  easy_install pip \
            && pip install docker-py==1.0.0 \
		&& pip install ipython==2.4.1 \
		&& pip install python-etcd==0.3.2 \
		&& pip install requests==2.1.0 \
		&& pip install simplejson==3.6.5 \
            && pip install supervisor==3.1.3 \
            && apt-get -y autoremove \
            && apt-get clean && mkdir -p /opt/dispatch

COPY    ./dispatch/   /opt/dispatch

RUN     cd /opt/dispatch \
		&& ls /opt && ls /opt/dispatch \
            && pip install -r requirements.txt 
EXPOSE  80, 8080
CMD  ["python", "/opt/dispatch/dispatch.py"]
