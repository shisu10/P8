FROM python:3.10-slim-bookworm
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]