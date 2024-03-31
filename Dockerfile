FROM python:3.9-slim

# Set a non-root user with limited permissions
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin -c "Docker image user" app
WORKDIR /app

# Copy the Python script and requirements.txt file into the container's /app directory
COPY ssl_scan.py requirements.txt /app/
ADD /logs /app/logs
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R app:app /app
USER app

# Run the Python script when the container starts
CMD ["python", "ssl_scan.py"]

