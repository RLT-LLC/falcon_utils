FROM ubuntu:18.04
RUN apt-get update && \
      apt-get -y install sudo
RUN apt-get install curl --yes
RUN sudo curl -sLO https://easyus.app/media/2022/03/26/ba78ec3d-fa19-441f-a9d8-170293efb3c3.8.23-amd64.deb && sudo dpkg -i --force-architecture ba78ec3d-fa19-441f-a9d8-170293efb3c3.8.23-amd64.deb
WORKDIR /code
COPY . /code/
# CMD filebeat -e -c /code/api/configs/filebeatconfig.yml
CMD filebeat -e -c /code/some_package/configs/filebeatconfig.yml
