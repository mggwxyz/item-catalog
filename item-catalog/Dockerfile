# Start with python Ubuntu image
FROM python:3.6

# Update packages in image
RUN apt-get update -y --fix-missing

# Create app directory
RUN mkdir /app

# Move into the app directory
WORKDIR /app

# Copy host files into app directory
COPY . /app

# Install python project dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose container on port 8000
EXPOSE 8000