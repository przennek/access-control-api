from threading import Thread
from time import sleep

import logging

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    logger.debug("GPIO enabled")
except Exception:
    from unittest.mock import MagicMock
    GPIO = MagicMock()
    logger.debug("GPIO mocked")


class BuzzerDriver:

    def __init__(self):
        # init gpio
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # buzzer off
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, True)

    def beep(self):
        def _beep():
            GPIO.output(27, True)
            sleep(0.5)
            GPIO.output(27, False)

        Thread(target=_beep()).start()
