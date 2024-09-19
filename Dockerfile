# FROM ghcr.io/justuskilianwolff/rye-image:latest
FROM ubuntu:22.04

# set bash as shell
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl && \
    curl -sSf https://rye.astral.sh/get | RYE_TOOLCHAIN_VERSION="cpython@3.11.9" RYE_INSTALL_OPTION="--yes" bash

# Set environment variables
ENV PATH="/root/.rye/shims:${PATH}"
ENV RYE_HOME="/root/.rye"

# Verify Rye installation
RUN rye --version

# Set the default command to /bin/bash so you can enter the shell
CMD ["/bin/bash"]