# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

# Install git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt install -y git

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.git,target=.git \
    uv sync --locked --no-install-project

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["uv", "run", "fastapi", "run", "wikiproxy", "--port", "3672", "--proxy-headers"]
