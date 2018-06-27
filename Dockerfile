FROM node:stretch

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get -y install python3 python3-pip libpq-dev

RUN npm install -g gulp-cli

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN npm install

RUN gulp js && gulp sass

RUN apt-get clean

EXPOSE 5000

ENV FLASK_APP awards

CMD python3 -m flask run -h 0.0.0.0
