FROM python:3-slim-buster

COPY helloworld.py .

ENTRYPOINT ["python"]
CMD ["helloworld.py"]


