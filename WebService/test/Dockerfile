FROM nginx
WORKDIR /CoffeeApp

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y pip
RUN pip install cassandra-driver
RUN pip install cqlsh
