FROM python:3.8.4
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY ./  /usr/src/app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`

curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE

`/chromedriver_linux64.zip

RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

ENV DISPLAY=:99

