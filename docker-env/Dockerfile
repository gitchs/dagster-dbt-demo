FROM python:3.10
LABEL authors="tiny.chen@protonbase.io"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y && apt install -y openssh-server && pip3 install poetry --index-url=https://pypi.tuna.tsinghua.edu.cn/simple/
COPY ./start.py /start.py
CMD python3 /start.py


