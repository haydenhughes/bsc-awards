FROM python:3

WORKDIR /usr/src/app

RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
RUN apt-get update && apt-get install -y nodejs

RUN npm install -g gulp-cli

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN npm install

RUN gulp js && gulp sass

RUN apt-get clean

EXPOSE 5000

ENV FLASK_APP awards

CMD python3 -m flask run -h 0.0.0.0
