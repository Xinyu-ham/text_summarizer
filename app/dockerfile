FROM python:3.9.0-slim
COPY . .
RUN pip3 install -r requirements.txt
ENV NLTK_DATA='./nltk_data'
EXPOSE 5000
CMD ["gunicorn", "wsgi:app", "-c", "gunicorn_config.py"]