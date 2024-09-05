FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN python3 init_db.py

ENV FLASK_APP=app.python

CMD ["gunicorn", "app:app"]
