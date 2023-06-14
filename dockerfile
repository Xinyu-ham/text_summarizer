FROM python:3.9.0-slim
COPY . .
RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader -d /usr/share/nltk_data punkt
EXPOSE 5000
CMD ["gunicorn", "wsgi:app", "-c", "gunicorn_config.py"]