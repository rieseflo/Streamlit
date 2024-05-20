# Usage
# docker build -t rieseflo/meteorite-display .
# docker push rieseflo/ meteorite-display:latest
# docker run --name meteorite-display -p 9000:8501 -d rieseflo/meteorite-display:latest

FROM python:3.10.11-slim

WORKDIR /usr/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["sh", "-c", "streamlit run --server.port 8501 /usr/app/meteorite-display.py"]