# Use an official Python runtime as a parent image
FROM python:3.6-slim

ARG RMQ_HOST
ENV RMQ_HOST=${RMQ_HOST}
ARG RMQ_TELNET_OPERATOR_RMQ_EXCHANGE
ENV RMQ_TELNET_OPERATOR_RMQ_EXCHANGE=${RMQ_TELNET_OPERATOR_RMQ_EXCHANGE}
ARG RMQ_TELNET_OPERATOR_RMQ_QUEUE_IN
ENV RMQ_TELNET_OPERATOR_RMQ_QUEUE_IN=${RMQ_TELNET_OPERATOR_RMQ_QUEUE_IN}
ARG RMQ_TELNET_OPERATOR_REDIRECT_TO_EXCHANGE
ENV RMQ_TELNET_OPERATOR_REDIRECT_TO_EXCHANGE=${RMQ_TELNET_OPERATOR_REDIRECT_TO_EXCHANGE}
ARG RMQ_TELNET_OPERATOR_REDIRECT_TO_QUEUE
ENV RMQ_TELNET_OPERATOR_REDIRECT_TO_QUEUE=${RMQ_TELNET_OPERATOR_REDIRECT_TO_QUEUE}

RUN apt-get update
RUN apt-get install -y git

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["python", "rmq_telnet_operator.py"]