# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
COPY mysite /mysite/

COPY requirements/django-worker/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y bash \
	&& pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]