FROM python:3.7.1

ADD docker /tmp/docker
RUN apt-get update; apt-get install -y $(awk '{print $1'} /tmp/docker/linux_packages.txt)
RUN pip install -r /tmp/docker/python_packages.txt

ADD model /home
ADD mine.py /home

WORKDIR /home/

#Stay up forever
CMD ["tail", "-f", "/dev/null"]
