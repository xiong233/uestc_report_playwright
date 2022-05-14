FROM mcr.microsoft.com/playwright/python:v1.22.0-focal

ENV APP_PATH="/"

ENV LC_ALL="C.UTF-8"

COPY ./main.py ./slide.py ./scheduler.py ./requirements.txt $APP_PATH/
ARG DEBIAN_FRONTEND=noninteractive

RUN pip install -r /requirements.txt

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 

WORKDIR ${APP_PATH}

ENTRYPOINT [ "python3", "/scheduler.py"]