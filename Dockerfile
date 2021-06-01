FROM python:3.9.5
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /opt/app
COPY /src/* /opt/app/