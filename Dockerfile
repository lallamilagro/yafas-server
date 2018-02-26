FROM python:3.6-slim

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV BCRYPT_ROUNDS=4 SECRET_KEY=we-hate-you

CMD alembic upgrade head && gunicorn app:api -w 4 -b 0.0.0.0:5000
