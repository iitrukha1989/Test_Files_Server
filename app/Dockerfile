FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app/
EXPOSE 8000
ENTRYPOINT [ "python3" ]
CMD [ "server.py" ]
