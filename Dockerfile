FROM python:latest
RUN apt -y update && apt -y upgrade && \
    mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
CMD ["gunicorn app:app -b 0.0.0.0:8000", ]