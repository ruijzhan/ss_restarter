FROM debian:buster-slim
RUN set -x &&\
    apt-get update &&\
    apt-get install -y python3-pip git &&\
    pip3 install pipenv &&\
    git clone https://github.com/ruijzhan/ss_restarter.git &&\
    cd ss_restarter &&\
    pipenv install &&\
    apt-get remove --purge git -y &&\
    apt-get autoremove --purge -y &&\
    apt-get clean &&\
    apt-get clean all &&\
    rm -rf /var/lib/apt/lists/*
WORKDIR	/ss_restarter
ENTRYPOINT ["pipenv", "run", "python"]
