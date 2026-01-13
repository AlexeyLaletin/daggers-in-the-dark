FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive

# Common dev tools + postgres client + redis cli + build essentials
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    gnupg \
    jq \
    less \
    lsof \
    nano \
    openssh-client \
    procps \
    python3 \
    python3-pip \
    python3-venv \
    sqlite3 \
    build-essential \
    postgresql-client \
    redis-tools \
  && rm -rf /var/lib/apt/lists/*

# Node.js (LTS 22.x). If you pick another stack later, you can remove this block.
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
  && apt-get update \
  && apt-get install -y --no-install-recommends nodejs \
  && rm -rf /var/lib/apt/lists/*

# Enable corepack (pnpm/yarn) if available
RUN corepack enable || true
