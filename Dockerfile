#Use base Ubuntu image 
FROM python:latest as web_stg
LABEL maintainer "David Eads <dceads72@gmail.com>"
#add flask
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential 
RUN pip install python-dotenv
RUN pip install requests
RUN pip install pg8000
RUN pip install pyshp
RUN pip install envs
RUN pip install postgres
RUN pip install postgis
RUN pip install psycopg2
RUN pip freeze > requirements.txt
RUN echo "flask" >> requirements.txt
RUN echo "redis" >> requirements.txt
RUN pip install -r requirements.txt
#CMD python app.py
RUN mkdir /app
COPY . /app
#COPY cb_2018_us_state_500k.shp postgres-data/postgres:/var/lib/postgresql/data
WORKDIR /app
#Expose flask port & postgres port
EXPOSE 5000
