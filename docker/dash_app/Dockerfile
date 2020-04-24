# see Example https://www.callicoder.com/deploy-containerized-go-app-kubernetes/
# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# Start from the python:3.8-slim image
FROM python:3.8-slim

# Add Maintainer Info
LABEL maintainer="Mashkov Dmitry <mashkoffdmitry@gmail.com>"

# Set the Current Working Directory inside the container
WORKDIR /code

COPY ./docker/dash_app/requirements.txt  ./

# Download all dependancies. Dependencies will be cached
RUN pip install -r requirements.txt

# Copy the source to the Working Directory inside the container
COPY ./docker/dash_app /code

# Expose port 8080 to the outside world
EXPOSE 5000

# Command to run the executable
#CMD gunicorn -b 0.0.0.0:5000 wsgi:app -w 2 --reload
CMD python app.py