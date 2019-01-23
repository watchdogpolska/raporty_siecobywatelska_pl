#!/bin/bash

set +x

PROJECT_ID=raporty-kamil
APP_NAME=raporty-app
APP_TAG=$(git rev-parse HEAD |fold -w 7 | head -n 1)
echo "Current TAG: ${APP_TAG}"

docker build -t gcr.io/${PROJECT_ID}/${APP_NAME}:latest -f Dockerfile-prod .

docker tag ${APP_NAME} gcr.io/${PROJECT_ID}/${APP_NAME}:${APP_TAG}

docker push gcr.io/${PROJECT_ID}/${APP_NAME}:latest
docker push gcr.io/${PROJECT_ID}/${APP_NAME}:${APP_TAG}

