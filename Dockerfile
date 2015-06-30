FROM python:latest
MAINTAINER rpollak@genecloud.com
RUN pip install Flask
RUN pip install sqlalchemy
RUN pip install Flask-SQLAlchemy
RUN pip install PyMySql
ADD . /GenomeParser
WORKDIR /GenomeParser
CMD python parser.py
