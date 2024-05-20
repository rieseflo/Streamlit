# Usage
# docker build -t rieseflo/streamlit_app .
# docker push rieseflo/streamlit_app:latest
# docker run --name streamlit_app -p 9000:8501 -d rieseflo/streamlit_app:latest

FROM python:3.10.11-slim

WORKDIR /usr/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["sh", "-c", "streamlit run --server.port 8501 /usr/app/meteorite-display.py"]