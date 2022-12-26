###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.6-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy all
COPY . .

# copy entrypoint.prod.sh
COPY ./entrypoint.sh .
# RUN chmod +x entrypoint.sh

# # run entrypoint.prod.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]