FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/requirements.txt

RUN pip install -r backend/requirements.txt

COPY backend/ ./backend

COPY data/ ./data

COPY llm_models/ ./llm_models

EXPOSE 8000

CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
