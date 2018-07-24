FROM python:3

RUN mkdir /kraven
WORKDIR /kraven
ADD . /kraven

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "./manage.py runserver 0.0.0.0:8000"]