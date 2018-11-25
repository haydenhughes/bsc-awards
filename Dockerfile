FROM python:3

ENV FLASK_APP awards

WORKDIR /usr/src/app

COPY . .

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get update && apt-get install -y nodejs && \
    npm install -g gulp-cli && \
    pip3 install --no-cache-dir -r requirements.txt && \
    npm install && \
    gulp js && \
    gulp sass && \
    apt-get clean

EXPOSE 5000

CMD python3 -m flask run -h 0.0.0.0
