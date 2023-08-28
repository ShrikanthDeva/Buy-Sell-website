FROM python:3.8.13-slim-buster

RUN mkdir -p /home/django/mysite \
    && mkdir -pv /var/log/gunicorn \
    && mkdir -pv /var/run/gunicorn

WORKDIR /home/django/mysite

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "-c", "config/gunicorn/dev.py"]
# FROM python:3.8.13-slim-buster

# RUN mkdir -p /home/djangopro/mysite
# RUN mkdir -pv /var/log/gunicorn 
# RUN mkdir -pv /var/run/gunicorn

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /home/djangopro/mysite

# COPY requirements.txt /home/djangopro/
# COPY . .

# RUN pip install -r requirements.txt

# CMD ["gunicorn", "-c", "config/gunicorn/dev.py"]