FROM python:3.9.5
EXPOSE 8000/tcp

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /opt/app
COPY /src/* /opt/app/

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0"]
