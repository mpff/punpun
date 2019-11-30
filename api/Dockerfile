
# Pull base image
FROM python:3.6

LABEL MAINTAINER="Manuel Pfeuffer <pfeufferm@<hu-berlin.de>"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /punpun.me/api/

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /punpun.me/api/requirements.txt
RUN pip install -r requirements.txt

# Copy project
COPY . /punpun.me/api/
