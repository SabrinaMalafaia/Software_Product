FROM python:3.11-alpine

RUN python -m pip install --upgrade pip
RUN pip install Flask
RUN pip install requests
RUN pip install mysql-connector-python

COPY _rotas.py /_rotas.py

CMD [ "python", "_rotas.py" ]