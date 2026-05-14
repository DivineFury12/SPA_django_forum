FROM python:3.13-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod 655 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml ./
RUN uv sync

FROM python:3.13-slim-bookworm AS prod

ENV VIRTUAL_ENV="/app/.venv"
ENV PATH="/app/.venv/bin:$PATH"

ENV DB_HOST="postgres"
ENV DB_PORT="5432"
ENV DB_NAME="postgres"
ENV DB_USER="postgres"
ENV DB_PASSWORD="postgres"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src ./src

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]