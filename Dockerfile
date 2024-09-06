FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN python3 init_db.py

ENV FLASK_APP=app.python

EXPOSE 8000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
