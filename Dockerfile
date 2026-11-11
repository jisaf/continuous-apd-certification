# capd in a container, for CI systems that prefer images:
#   docker build -t capd .
#   docker run --rm -v "$PWD:/work" -w /work capd run --config capd.yaml
FROM python:3.12-slim
WORKDIR /opt/capd
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . && useradd --create-home capd
USER capd
WORKDIR /work
ENTRYPOINT ["capd"]
