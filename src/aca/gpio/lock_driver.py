import logging

from aca.gpio.buzzer_driver import BuzzerDriver

logger = logging.getLogger(__name__)

gpio_mocked = False

try:
    import RPi.GPIO as GPIO
except Exception:
    from unittest.mock import MagicMock

    GPIO = MagicMock()
    gpio_mocked = True


class LockDriver:
    # services
    bd: BuzzerDriver

    def __init__(self, bd: BuzzerDriver):
        self.bd = bd

        # init gpio
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def open_lock(self):
        if gpio_mocked:
            logger.warning("GPIO is mocked")

        self.bd.beep()
        # open lock
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, True)

    def close_lock(self):
        if gpio_mocked:
            logger.warning("GPIO is mocked")

        self.bd.beep()
        # door closed
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, False)
