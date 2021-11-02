ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install requirements for add-on
# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN apk add --no-cache git \
					   gcc \
					   musl-dev \
					   python3-dev
RUN pip install git+https://github.com/hex-in/libscrc.git
RUN pip install git+https://github.com/eclipse/paho.mqtt.python.git
RUN pip install influxdb
RUN pip install influxdb-client
RUN apk del gcc \
			musl-dev \
			python3-dev

# RUN pip install requests-async

# Python 3 HTTP Server serves the current working dir
# So let's set it to our add-on persistent data directory.
WORKDIR /data

# RUN rm -Rf Sofar_LSW3; git clone https://github.com/MichaluxPL/Sofar_LSW3.git /data/Sofar_LSW3
RUN rm -Rf Sofar_LSW3; git clone http://nas.marm:30000/MARM.pl/Sofar_LSW3.marm.git /data/Sofar_LSW3

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ] 
