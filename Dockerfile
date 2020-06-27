FROM --platform=linux/arm/v6 arm32v6/alpine:latest AS stage1

RUN apk update
RUN apk add --no-cache git bash build-base libffi-dev openssl-dev bzip2-dev zlib-dev readline-dev sqlite-dev

RUN adduser python_user --disabled-password
#RUN ln -s /proc/self/fd /dev/fd

WORKDIR /home/python_user
USER python_user

RUN git clone git://github.com/pyenv/pyenv.git .pyenv

ENV HOME /home/python_user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV PYTHON_BUILD_CACHE_PATH $PYENV_ROOT/.cache
ENV LANG C.UTF-8

RUN mkdir $PYTHON_BUILD_CACHE_PATH
COPY cache $PYENV_ROOT/.cache/

#RUN env PYTHON_CFLAGS="-Os" pyenv install 3.8.3
RUN env PYTHON_CONFIGURE_OPTS="--enable-optimizations" pyenv install 3.8.3
RUN pyenv global 3.8.3
RUN pyenv rehash
RUN pip install --upgrade pip
RUN pip install pipenv

RUN rm -r $PYTHON_BUILD_CACHE_PATH

COPY *.py bot/
COPY Pipfile Pipfile.lock bot/

WORKDIR bot

RUN pipenv install --deploy --python 3.8.3



FROM --platform=linux/arm/v6 arm32v6/alpine:latest

RUN apk update
RUN apk add --no-cache bash libffi openssl bzip2 zlib readline sqlite

RUN adduser python_user --disabled-password

USER python_user

ENV HOME /home/python_user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV LANG C.UTF-8

COPY --from=stage1 /home/python_user /home/python_user

WORKDIR /home/python_user/bot

ENTRYPOINT [ "pipenv", "run", "python", "bot.py" ]
