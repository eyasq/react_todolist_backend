# Python base image
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Django dev server port
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]

# Start Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
