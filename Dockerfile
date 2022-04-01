FROM python:3.9

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/bianka_site

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/bianka_site

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]