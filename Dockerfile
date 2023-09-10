FROM python:3.8
RUN apt-get update
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 80
ENTRYPOINT python manage.py runserver 0.0.0.0:80