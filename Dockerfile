FROM node:14.4.0-stretch AS builder
WORKDIR /home/node/app/
COPY . .
RUN npm install -g gulp-cli && \
  npm install && \
  gulp js && \
  gulp sass

FROM python:3.8.2-alpine3.10
ENV FLASK_APP awards
WORKDIR /usr/src/app
COPY . .
COPY --from=builder /home/node/app/awards/static awards/static
RUN apk add --no-cache python3 postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps
EXPOSE 5000
CMD python3 -m flask run -h 0.0.0.0
