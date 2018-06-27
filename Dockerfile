FROM node:stretch

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get -y install python3 python3-pip

RUN npm install -g gulp-cli

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN npm install

RUN gulp js
RUN gulp sass

EXPOSE 5000

ENV FLASK_APP awards
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD python3 -m flask run -h 0.0.0.0
