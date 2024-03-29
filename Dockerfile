FROM python:3.7

RUN mkdir usr/app
WORKDIR usr/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python app.py