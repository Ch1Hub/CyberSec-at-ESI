# Remediated base image for container vulnerability scanning
FROM python:3.10-alpine
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]
