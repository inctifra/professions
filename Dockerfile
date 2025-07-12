# Use official Python slim image
ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs npm \
    && apt-get clean

# Create app directory
RUN mkdir -p /code
WORKDIR /code

# Install Python dependencies
COPY requirements/ /code/requirements/
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Copy the rest of the app
COPY . /code

# Expose port
EXPOSE 8000

# Set entrypoint and command
ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "config.wsgi"]
