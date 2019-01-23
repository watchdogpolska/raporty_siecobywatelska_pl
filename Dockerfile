FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ADD requirements/base.txt requirements/local.txt requirements/test.txt /app/requirements/

RUN pip install --upgrade pip --disable-pip-version-check --no-cache-dir && \
pip install -r requirements/local.txt -r requirements/test.txt --disable-pip-version-check --no-cache-dir
