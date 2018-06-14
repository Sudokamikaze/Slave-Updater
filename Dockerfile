MAINTAINER Sudokamikaze <Sudokamikaze@protonmail.com>
FROM renskiy/cron:alpine

RUN apk add --no-cache --update python py-pip bash
RUN pip install docker git configparser

COPY main.py /tmp/
COPY env.config /tmp/
RUN chmod +x /tmp/main.py

RUN echo "0 0 1-30/3 * * python /tmp/main.py" > /etc/crontabs
CMD ["start-cron"]