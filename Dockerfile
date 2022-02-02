FROM python:3.9.4-alpine

ARG APP_HOME="/app"
ARG APP_USER="appuser"

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk add --no-cache --virtual builds-deps build-base \
    && apk --no-cache --update add curl git libssl1.1 python3-dev \
                                   musl-dev libffi-dev libressl-dev \
                                   openssl-dev cargo \
    && pip install pip==21.2.4 \
    && pip install cython \
    && apk del builds-deps build-base \
    && addgroup -S appgroup && adduser -S ${APP_USER} -G appgroup

ENV PYTHONPATH=${APP_HOME}

RUN apk --no-cache add --update --virtual builds-deps build-base && \
    pip install poetry && \
    apk del builds-deps build-base

COPY pyproject.toml poetry.lock /

RUN apk --no-cache add --update --virtual builds-deps build-base \
    && poetry config virtualenvs.create false \
    && poetry install \
    && apk del builds-deps build-base

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY --chown=10001:10001 . ${APP_HOME}

USER ${APP_USER}
WORKDIR ${APP_HOME}

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["help"]
