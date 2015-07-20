FROM ubuntu
RUN apt-get update
RUN apt-get install -y python-dev python-pip libffi-dev libssl-dev
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
CMD ["python", "example_server.py"]