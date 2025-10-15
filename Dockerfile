FROM ghcr.io/seravo/ubuntu:noble

ARG APT_PROXY
LABEL org.opencontainers.image.description "gitlint"

RUN sed -i 's/main$/main universe/g' /etc/apt/sources.list && \
    apt-setup && \
    apt-get --assume-yes install \
      gitlint \
      gosu && \
    apt-cleanup

RUN useradd user && \
    mkdir -p /workdir && \
    mkdir -p /config

COPY .gitlint /config/gitlint
COPY --chmod=0755 entrypoint.sh /entrypoint.sh

WORKDIR /workdir
USER root
ENTRYPOINT ["/entrypoint.sh"]
CMD ["lint"]
