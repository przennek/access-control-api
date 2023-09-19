# Use the official Raspbian Buster image as the base image
FROM przennek/rasbian-buster:latest as builder

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install uwsgi python3 python3-pip libgl1-mesa-glx -y
RUN python3 -m pip install opencv-contrib-python
RUN python3 -m pip install picamera
RUN python3 -m pip install "picamera[array]"

# Expose the port that uWSGI will listen on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=/app/aca/access_control_api.py
ENV FLASK_ENV=production

# Copy the rest of the application files into the container
COPY ./src/aca ./aca
COPY ./templates ./aca/templates
COPY ./static ./aca/static
COPY ./config/requirements.txt ./requirements.txt
COPY ./config/uwsgi.ini ./aca/uwsgi.ini

RUN pip install -r requirements.txt
RUN apt-get -y install python3-rpi.gpio rpi.gpio-common python3-pyaudio

# Start uWSGI to run the Flask app
WORKDIR /app
CMD ["uwsgi", "--ini", "./aca/uwsgi.ini"]
