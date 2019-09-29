#!/bin/bash

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t haydenhughes/bsc-awards:$TRAVIS_TAG -t haydenhughes/bsc-awards:latest  .
docker push haydenhughes/bsc-awards:$TRAVIS_TAG
docker push haydenhughes/bsc-awards:latest
