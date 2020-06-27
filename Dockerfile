FROM --platform=linux/arm/v6 arm32v6/python:3.8.3-alpine AS build1

RUN apk -U upgrade
RUN apk add build-base libffi-dev openssl-dev

RUN adduser python_user --disabled-password
USER python_user
WORKDIR /home/python_user

ENV PIP_NO_CACHE_DIR false
ENV PIP_USER true
ENV PATH /home/python_user/.local/bin:$PATH

RUN pip install --upgrade pip
RUN pip install pipenv

RUN mkdir app
WORKDIR app
COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy



FROM --platform=linux/arm/v6 arm32v6/python:3.8.3-alpine

RUN apk -U upgrade
RUN apk add libffi openssl

RUN adduser python_user --disabled-password
USER python_user

ENV PATH /home/python_user/.local/bin:$PATH

COPY --from=build1 /home/python_user /home/python_user

WORKDIR /home/python_user/app

COPY . .

ENTRYPOINT [ "pipenv", "run", "python", "bot.py" ]
