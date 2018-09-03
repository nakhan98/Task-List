FROM debian:latest
RUN useradd -ms /bin/bash -u1000 tester

RUN apt-get update && apt-get upgrade -y && apt-get clean -y
RUN apt-get install sudo aptitude bash-completion locales \
    virtualenv python wget git -y
RUN echo 'tester ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
RUN aptitude clean


# See: https://hub.docker.com/r/pfcarrier/debian-locale/builds/biksnydxmevjscmbkbclu6c/
# https://github.com/moby/moby/issues/4032
# ENV DEBIAN_FRONTEND noninteractive
RUN echo "en_GB.UTF-8 UTF-8" > /etc/locale.gen && \
    DEBIAN_FRONTEND=noninteractive locale-gen en_GB.UTF-8 && \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales && \
    DEBIAN_FRONTEND=noninteractive /usr/sbin/update-locale LANG=en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8

USER tester
WORKDIR /home/tester
COPY src/ /home/tester/task_list/
COPY requirements.txt .
RUN virtualenv django_env
RUN django_env/bin/pip install -r ~/requirements.txt
# RUN /home/tester/django_env/bin/python task_list/manage.py migrate
# CMD ["/home/tester/django_env/bin/python", "task_list/manage.py", "runserver"]
CMD /home/tester/django_env/bin/python task_list/manage.py migrate && \
    /home/tester/django_env/bin/python task_list/manage.py runserver 0.0.0.0:8000

EXPOSE 8000
