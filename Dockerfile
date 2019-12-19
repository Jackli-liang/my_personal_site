# 
FROM python:3.7



ENV PYTHONUNBUFFRED 1


RUN mkdir /code
WORKDIR /code

RUN pip install pip -U


ADD requirements.txt /code/


RUN pip install -r requirements.txt


RUN pip install -r requirements.txt


ADD . /code/
