FROM python:latest
COPY . .
WORKDIR .

EXPOSE 5000
RUN pip install -r requirements.txt

CMD ["python", "app.py"]