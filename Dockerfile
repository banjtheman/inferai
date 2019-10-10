FROM python:3.7.1

ADD docker /tmp/docker
RUN pip install -r /tmp/docker/python_packages.txt

ADD model /home
ADD mine.py /home

WORKDIR /home/

#Stay up forever
CMD ["tail", "-f", "/dev/null"]