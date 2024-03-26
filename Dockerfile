# Define the steps that docker needs in order to build our image

# Define the base image pulled of Docker Hub
FROM python:3.9-alpine3.13
# Who will be mainting this image
LABEL mainteiner="joseserrano.com"

ENV PYTHONUNBUFFERED 1

# Copy our requirements.txt to our local machine to /tmp/requirements.txt
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy the app directory
COPY ./app /app
# app is the location where our Django project is going to be sent
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# runs a RUN command on the alpine image thaht we are using when we are building our image
# Create a new venv to install our requirements
RUN python -m venv /py && \
    # Specify full path of venv and update pip
    /py/bin/pip install --upgrade pip && \
    # Install the requirements to our docker image
    /py/bin/pip install -r /tmp/requirements.txt && \
    # if DEV equals true install requirements.dev.txt
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # remove the tmp directory
    rm -rf /tmp && \
    # calls the add user command to which adds a new user inside our image
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Create variable to map our venv path
ENV PATH="/py/bin:$PATH"

# The subsequent commands were executed under the root user until the execution of this command, which operates under the user account created on line 29
USER django-user

