FROM python:3.9

WORKDIR /app

COPY static ./static 
COPY templates ./templates 
COPY ["app.py", "requirements.txt", "./"]

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

CMD python app.py