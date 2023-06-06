FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /clients_portal

# install dependences
COPY ./requirements.txt /clients_portal/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /clients_portal/requirements.txt

## install google chrome
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable

## install chromedriver
#RUN apt-get install -yqq unzip
#RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#COPY /usr/local/bin/chromedriver /clients_portal/src/functional_tests/

#RUN apt-get install gettext -y

# set display port to avoid crash
ENV DISPLAY=:99

# set open port
EXPOSE 8025











