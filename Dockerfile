
FROM python:3.12.3

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt


ENV FLASK_APP=todo.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=True
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run"]