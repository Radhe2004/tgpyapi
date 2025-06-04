FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh

USER 1001

CMD ["./start.sh"]