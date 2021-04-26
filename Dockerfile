# syntax=docker/dockerfile:1
FROM ubuntu:20.10
RUN apt update -y

# Installing text editors
RUN apt install vim -y
RUN apt install emacs -y
RUN apt install nano -y
RUN apt install less -y

# Installing networking tools
RUN apt install curl -y
RUN apt install net-tools -y
RUN apt install netcat -y

# Installing Python3.9 and Pip
RUN apt install python3.9 -y
RUN apt install python3-pip -y

# Copy the contents 
COPY . .
WORKDIR "/server"

# Install all the dependencies
RUN python3.9 -m pip install -r requirements.txt

# Run the flask server
CMD [ "python3.9", "app.py"]

