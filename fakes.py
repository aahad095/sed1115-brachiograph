# fakes.py
# Pretend hardware for the laptop tests. These classes act like the
# machine.ADC, machine.Pin and machine.PWM objects, so functions that
# normally talk to the Pico can be checked on a laptop.
# Used only by the tests, never uploaded to the Pico.

import os
import sys

# let the tests import the project files from the folder above
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class FakeADC:
    """Returns whatever number we put in .value"""
    def __init__(self, value=0):
        self.value = value

    def read_u16(self):
        return self.value


class FakePin:
    """A button. .level is 1 when up and 0 when pressed (pull-up)."""
    def __init__(self, level=1):
        self.level = level

    def value(self):
        return self.level


class FakePWM:
    """Remembers the last duty_u16() value written to it."""
    def __init__(self):
        self.duty = None

    def duty_u16(self, duty):
        self.duty = duty
