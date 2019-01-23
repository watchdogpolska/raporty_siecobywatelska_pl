#!/bin/bash

set +x

PROJECT_ID=raporty-kamil
APP_NAME=raporty-app
APP_TAG=$(git rev-parse HEAD |fold -w 7 | head -n 1)

echo docker build -t ${APP_NAME}:latest -f Dockerfile-prod .

echo docker tag ${APP_NAME} gcr.io/${PROJECT_ID}/${APP_NAME}${APP_TAG}

echo docker push gcr.io/${PROJECT_ID}/${APP_NAME}:latest
echo docker push gcr.io/${PROJECT_ID}/${APP_NAME}:${APP_TAG}

