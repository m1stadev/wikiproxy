# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:0.9.26-python3.14-trixie-slim

RUN apt-get update
RUN apt-get upgrade -y
RUN apt install -y git

ENV UV_COMPILE_BYTECODE=1

CMD ["uvx", "--with", "git+https://github.com/m1stadev/wikiproxy.git", "--from", "fastapi[standard]", "fastapi", "run", "wikiproxy", "--port", "3672", "--proxy-headers"]
