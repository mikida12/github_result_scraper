FROM python:3.7

WORKDIR /app
RUN apt-get update
RUN apt-get install -y iceweasel
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
tar -xvzf geckodriver* && \
chmod +x geckodriver && \
mv geckodriver /usr/local/bin/

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

COPY . /app
CMD /wait && python logic.py
