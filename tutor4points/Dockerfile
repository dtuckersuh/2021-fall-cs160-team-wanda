FROM python:3.11-rc-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apk --update add build-base jpeg-dev zlib-dev libffi-dev

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]