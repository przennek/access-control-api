# Use the official Raspbian Buster image as the base image
FROM przennek/rasbian-buster:latest as builder

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get upgrade -y
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=critical

RUN apt-get -y install libasound2 alsa-utils pulseaudio
RUN apt-get -y install python3 python3-pip libgl1-mesa-glx -y
RUN apt-get install libssl-dev

RUN CFLAGS="-I/usr/local/opt/openssl/include" LDFLAGS="-L/usr/local/opt/openssl/lib" \
    UWSGI_PROFILE_OVERRIDE=ssl=true pip install uwsgi -Iv

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

# Install supervisord
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

RUN echo '* * * * * root PYTHONPATH="/app" /usr/bin/python3 /app/aca/jobs/open_close_politcs.py >> /var/log/cron.log 2>&1' > /etc/cron.d/cronjob \
    && chmod 0644 /etc/cron.d/cronjob

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start uWSGI and cron
WORKDIR /app
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]