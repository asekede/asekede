FROM python:3
ENV PYTHONUNBUFFERED 1
LABEL maintainer="assylkhan.abdrakhmanov@gmail.com"
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
VOLUME /code
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]