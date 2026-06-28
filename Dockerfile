FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 8501

CMD ["streamlit","run","backend/app.py","--server.address=0.0.0.0"]