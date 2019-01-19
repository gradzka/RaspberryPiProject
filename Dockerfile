FROM raspbian/stretch:latest

RUN apt-get update
RUN apt-get -y install nginx
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install --no-cache-dir picamera flask flask_cors netifaces wiringpi paho-mqtt
RUN mkdir /Project
RUN mkdir /Project/MQTT
RUN mkdir /Project/WEBSITE
RUN apt-get -y install libraspberrypi0
RUN rm -v /etc/nginx/nginx.conf

COPY ./Addins/nginx.conf /etc/nginx/

COPY ./MQTT /Project/MQTT
COPY ./WEBSITE /Project/WEBSITE
COPY ./camera.py /Project
COPY ./simple_server.py /Project
EXPOSE 80
EXPOSE 1247

CMD service nginx start && python3 Project/simple_server.py

