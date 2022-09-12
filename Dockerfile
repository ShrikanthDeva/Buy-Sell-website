FROM python:3.10.7-slim-buster

RUN mkdir -p /home/djangopro/mysite
RUN mkdir -pv /var/log/gunicorn 
RUN mkdir -pv /var/run/gunicorn

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/djangopro/mysite

COPY requirements.txt /home/djangopro/
COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "config/gunicorn/dev.py"]