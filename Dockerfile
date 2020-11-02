FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirement.txt /code/
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirement.txt
RUN pip install uwsgi
COPY . /code/