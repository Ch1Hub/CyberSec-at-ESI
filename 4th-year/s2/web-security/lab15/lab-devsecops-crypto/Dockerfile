FROM python:3.10-alpine
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev
RUN adduser -D myuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
USER myuser
EXPOSE 5000
CMD ["python", "app.py"]