FROM alpine:latest
RUN adduser -D -u 1001 tester

RUN apk update && apk add python py-virtualenv python-dev build-base \
    linux-headers pcre-dev

USER tester
WORKDIR /home/tester
COPY requirements.txt .
RUN virtualenv django_env
RUN django_env/bin/pip install -r ~/requirements.txt
CMD /home/tester/django_env/bin/python task_list/manage.py migrate && \
    /home/tester/django_env/bin/uwsgi --ini task_list/task_list_uwsgi.ini

EXPOSE 48080
