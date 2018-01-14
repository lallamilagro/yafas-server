FROM python:3.6-slim

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=/app/app.py SECRET_KEY=we-hate-you JWT_SECRET_KEY=I-hate-frontend

CMD flask db upgrade && gunicorn app:app -w 4 -b 0.0.0.0:5000
