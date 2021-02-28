# set base image (host OS)
FROM python:3.8-alpine
LABEL maintainer="andres.salazar.spinetti@gmail.com"

RUN apk --no-cache --update add build-base libffi-dev musl-dev

# set the working directory in the container
WORKDIR /src

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY ./crontab /etc/crontabs/root

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD ["crond", "-f", "-d", "8"]
