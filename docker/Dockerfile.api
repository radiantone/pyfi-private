FROM python:3.10

RUN mkdir -p /var/log/supervisor
RUN apt-get update
RUN apt install -y supervisor
RUN apt install -y iputils-ping
RUN apt install -y telnet
#RUN apt install -y python3-pip
RUN apt install -y libpq-dev
RUN apt install -y libevent-dev libev-dev libevdev2
RUN apt install -y git
#RUN apt install -y xvfb
RUN apt clean

ADD pyfi /opt/pyfi/pyfi
ADD requirements.txt /opt/pyfi/requirements.txt
ADD setup.py /opt/pyfi/setup.py
ADD README.md /opt/pyfi/README.md
ADD scripts/supervisor.sh /opt/pyfi/supervisor.sh
ADD conf/pyfi.ini /opt/pyfi/pyfi.ini
ADD conf/pyfi.ini /root/pyfi.ini
WORKDIR /opt/pyfi
RUN pip3 install virtualenv
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

#RUN apt install -y python3.10
ADD conf/supervisord-api.conf /opt/pyfi/supervisord.conf
ADD conf/pyfi.ini /home/pyfi/pyfi.ini
ADD pyfi.polar /root/pyfi.polar

RUN useradd pyfi -d /home/pyfi
RUN chown -R pyfi /opt/pyfi /home/pyfi
RUN virtualenv --python=python3 venv
#RUN python3.9 -m venv venv
RUN venv/bin/pip uninstall -y setuptools
RUN venv/bin/pip install setuptools==59.1.1
RUN venv/bin/pip install --upgrade flask
RUN venv/bin/pip install -r requirements.txt
RUN update-rc.d -f supervisord remove
RUN venv/bin/pip uninstall -y pytz
RUN venv/bin/python setup.py install
#RUN curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash


#CMD ["bash", "/opt/pyfi/supervisor.sh"]
CMD ["/opt/pyfi/venv/bin/flow","--debug","-i", "/opt/pyfi/pyfi.ini","api","start","-ip","0.0.0.0","-p","8003"]
