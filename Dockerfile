FROM python:3-slim-buster

COPY app.py .

ENTRYPOINT ["python"]
CMD ["app.py"]


