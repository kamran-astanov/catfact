# Stage 1: Base build environment
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.10-slim
LABEL maintainer="Kamran Astanov"
LABEL description="A simple Flask app to fetch random cat facts"
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd --create-home appuser
USER appuser
EXPOSE 5000
CMD ["python", "myapp.py"]
