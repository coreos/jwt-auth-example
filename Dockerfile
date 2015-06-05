FROM python:2-onbuild
ADD . .
CMD ["python", "example_server.py"]