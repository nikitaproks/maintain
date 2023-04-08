FROM python:latest

# set the working directory
WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install dependencies
COPY ./requirements.txt /backend
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY . /backend

# start the server
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]