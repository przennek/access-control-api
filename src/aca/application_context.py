from injector import inject, singleton

from aca.api.model.input.lock_control_input import LockControlModel
from aca.gpio.buzzer_driver import BuzzerDriver
from aca.gpio.lock_driver import LockDriver


# di context, default scope singleton
@inject
def context(binder):
    buzzer_driver = BuzzerDriver()
    binder.bind(BuzzerDriver, to=buzzer_driver, scope=singleton)

    lock_driver = LockDriver(buzzer_driver)
    binder.bind(LockDriver, to=lock_driver, scope=singleton)

    binder.bind(LockControlModel, to=LockControlModel(lock_driver), scope=singleton)
