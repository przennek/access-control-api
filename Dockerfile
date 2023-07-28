# Build uWSGI and the application
FROM navikey/raspbian-buster as builder

# Set the working directory in the container
WORKDIR /app

# Install build dependencies for uWSGI
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3 python3-pip build-essential wiringpi

# Copy the requirements.txt file into the container
COPY config/requirements.txt .

# Install the Python dependencies
RUN python3 -m "pip" install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY ./src/aca ./aca

# Build and install uWSGI
RUN python3 -m "pip" install uwsgi

# Set the working directory for the final image
WORKDIR /app

# Expose the port that uWSGI will listen on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=/app/aca/access_control_api.py
ENV FLASK_ENV=production

# Start uWSGI to run the Flask app
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "/app/aca/access_control_api.py", "--callable", "app", "--processes", "2", "--threads", "1"]
