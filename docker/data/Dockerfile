# see Example https://www.callicoder.com/deploy-containerized-go-app-kubernetes/
# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# Start from the python:3.8-alpine image
FROM python:3.8-alpine

# Add Maintainer Info
LABEL maintainer="Mashkov Dmitry <mashkoffdmitry@gmail.com>"

# Set the Current Working Directory inside the container
WORKDIR /code

COPY ./docker/data/requirements.txt  ./

# Download all dependancies. Dependencies will be cached
RUN pip install -i https://test.pypi.org/simple/ --extra-index-url=https://pypi.org/simple/ tinkoff-invest-openapi-client &&  pip install -r requirements.txt

# Copy the source to the Working Directory inside the container
COPY ./docker/data /code

# Command to run the executable
CMD python get_data.py