FROM python:3.10-slim-bookworm
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]