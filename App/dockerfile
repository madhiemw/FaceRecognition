FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0
ENV MONGO_URL=mongodb://host.docker.internal:27017/

CMD ["flask", "run"]
