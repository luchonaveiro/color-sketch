FROM python:3.7-slim

RUN pip install tensorflow==2.1.0 &&\
    pip install numpy &&\
    pip install plotly &&\
    pip install dash &&\
    pip install pillow &&\
    pip install requests

COPY . /app

WORKDIR /app

EXPOSE 8050

CMD python3 app.py