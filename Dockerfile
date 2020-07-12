FROM --platform=linux/arm/v6 arm32v6/python:3.8.3-alpine AS base-os

RUN apk -U upgrade --no-cache



FROM --platform=linux/arm/v6 base-os AS user-setup

RUN adduser python_user --disabled-password

WORKDIR /home/python_user/app
RUN chown python_user:python_user .

ONBUILD ENV PATH /home/python_user/.local/bin:$PATH



FROM --platform=linux/arm/v6 user-setup AS dependencies-setup

# Dependencias em tempo de construcao
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Dependencias em tempo de execucão
ONBUILD apk add --no-cache libffi openssl

USER python_user

ENV PIP_NO_CACHE_DIR false
ENV PIP_USER true

RUN pip install --upgrade pip
RUN pip install pipenv

COPY --chown=python_user:python_user Pipfile Pipfile.lock ./

RUN pipenv install --deploy




FROM --platform=linux/arm/v6 user-setup AS app-setup

COPY --from=dependencies-setup /home/python_user /home/python_user
COPY --chown=python_user:python_user . .

USER python_user

ENTRYPOINT [ "pipenv", "run", "python", "bot.py" ]
