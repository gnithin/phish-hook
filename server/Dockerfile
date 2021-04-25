# syntax=docker/dockerfile:1
FROM ubuntu:20.10
RUN apt update -y

# Installing text editors
RUN apt install vim -y
RUN apt install emacs -y
RUN apt install nano -y
RUN apt install less -y

#Installing networking tools
RUN apt install curl -y
RUN apt install net-tools -y
RUN apt install netcat -y

#Installing Python3
RUN apt install python3 -y

ENTRYPOINT tail -f /dev/null

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3", "app.py"]

