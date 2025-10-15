FROM ghcr.io/seravo/ubuntu:noble

ARG APT_PROXY

RUN sed -i 's/main$/main universe/g' /etc/apt/sources.list && \
    apt-setup && \
    apt-get --assume-yes install \
      gitlint && \
    apt-cleanup

RUN useradd user && \
    mkdir -p /workdir && \
    mkdir -p /config

COPY .gitlint /config/gitlint
USER user

WORKDIR /workdir

ENTRYPOINT ["/usr/bin/gitlint"]
CMD ["lint"]
