FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh  # Fix line endings + permissions

# Option 1: Run as root (simplest)
CMD ["./start.sh"]

# Option 2: Run as non-root (if required)
# RUN chown -R 1001:1001 /app && chmod -R 755 /app
# USER 1001
# CMD ["./start.sh"]
