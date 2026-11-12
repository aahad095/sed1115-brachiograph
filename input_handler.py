# input_handler.py
# Owner: Claire Bryan
#
# Reads the two knobs and the two push buttons.
# Knob readings are smoothed with an 8-sample moving average.
# Buttons are debounced so one press counts as one press.
#
# SKELETON ONLY: the headers are final, the code inside is not written yet.
# Each function returns a placeholder so the whole program can be imported.

from array import array
import config

# "machine" only exists on the Pico. On a laptop we set it to None so the
# functions that don't touch hardware can still be unit tested.
try:
    import machine
except ImportError:
    machine = None


def init_inputs():
    """
    Owner:   Claire Bryan
    Purpose: Set up the knobs and buttons once, at start-up.
    Inputs:  none (pin numbers come from config.py)
    Returns: dict "inputs" with these keys:
               "adc_x", "adc_y"       - machine.ADC objects for the knobs
               "pen_btn", "mode_btn"  - machine.Pin inputs with pull-ups
               "buf_x", "buf_y"       - array("H") ring buffers, 8 samples each
               "index"                - int 0-7, next slot to overwrite
    How:     Create the ADC and Pin objects, create the two buffers filled
             with zeros, set index to 0, and put it all in one dict.
    Changes: creates the inputs dict (the only place it is created)
    """
    inputs = {
        "adc_x": None,
        "adc_y": None,
        "pen_btn": None,
        "mode_btn": None,
        "buf_x": array("H", [0] * config.BUFFER_SIZE),
        "buf_y": array("H", [0] * config.BUFFER_SIZE),
        "index": 0,
    }
    return inputs  # TODO: create the real ADC and Pin objects


def add_sample(buffer, index, value):
    """
    Owner:   Claire Bryan
    Purpose: Store one new knob reading in a ring buffer.
    Inputs:  buffer - array("H") of 8 counts
             index  - int 0-7, the slot to overwrite
             value  - int 0-65535, the new reading
    Returns: nothing
    How:     Overwrite buffer[index] with value. Nothing is appended, so the
             buffer never grows.
    Changes: buffer (one slot)
    """
    pass  # TODO


def average(buffer):
    """
    Owner:   Claire Bryan
    Purpose: Work out the average of the samples in a ring buffer.
    Inputs:  buffer - array("H") of 8 counts
    Returns: int 0-65535, the average count
    How:     Add up every value and integer-divide by the buffer length.
    Changes: nothing
    """
    return 0  # TODO


def apply_deadband(new_count, old_count):
    """
    Owner:   Claire Bryan
    Purpose: Stop the pen shaking when nobody is touching the knob.
    Inputs:  new_count - int 0-65535, the latest averaged reading
             old_count - int 0-65535, the value we used last loop
    Returns: int 0-65535, the count to use this loop
    How:     If the two are less than config.DEADBAND apart, return old_count
             (ignore the change). Otherwise return new_count.
    Changes: nothing
    """
    return new_count  # TODO


def read_smoothed_knob(adc, buffer, index, old_count):
    """
    Owner:   Claire Bryan
    Purpose: Get one clean reading from one knob.
    Inputs:  adc       - machine.ADC object for the knob
             buffer    - array("H") ring buffer for this knob
             index     - int 0-7, slot to overwrite this loop
             old_count - int 0-65535, the value used last loop
    Returns: int 0-65535, the smoothed count
    How:     Read adc.read_u16(), call add_sample(), call average(), then
             call apply_deadband() and return the result.
    Changes: buffer (through add_sample)
    """
    return old_count  # TODO


def detect_press(is_down, was_down, now_ms, last_press_ms):
    """
    Owner:   Claire Bryan
    Purpose: Decide if a button was just pressed (one press = one True).
    Inputs:  is_down       - bool, button is held down right now
             was_down      - bool, button was held down last loop
             now_ms        - int, current time from time.ticks_ms()
             last_press_ms - int, time of the last press we counted
    Returns: bool, True only on the loop where a new press starts
    How:     True if is_down and not was_down and at least config.DEBOUNCE_MS
             have passed since last_press_ms. Otherwise False.
    Changes: nothing (no hardware, so it can be unit tested on a laptop)
    """
    return False  # TODO


def check_button(pin, state, name, now_ms):
    """
    Owner:   Claire Bryan
    Purpose: Read one button and report if it was just pressed.
    Inputs:  pin    - machine.Pin for the button (pressed = 0)
             state  - the live state dict
             name   - str, "pen" or "mode", picks which keys to use
             now_ms - int, current time from time.ticks_ms()
    Returns: bool, True if a new press started this loop
    How:     Read the pin (0 means down). Call detect_press() with the
             remembered values. If it was a press, save now_ms as the last
             press time. Always save whether the button is down.
    Changes: state[name + "_was_down"] and state[name + "_press_ms"]
    """
    return False  # TODO


def read_inputs(inputs, state, now_ms):
    """
    Owner:   Claire Bryan
    Purpose: Read everything the user is doing, once per loop.
    Inputs:  inputs - dict from init_inputs()
             state  - the live state dict
             now_ms - int, current time from time.ticks_ms()
    Returns: tuple (x_count, y_count, pen_pressed, mode_pressed)
               x_count, y_count          - int 0-65535, smoothed knob counts
               pen_pressed, mode_pressed - bool, True if pressed this loop
    How:     Call read_smoothed_knob() for each knob, move inputs["index"]
             on by one (wrapping 7 back to 0), save the counts in the state,
             then call check_button() for each button.
    Changes: inputs["index"], state["x_count"], state["y_count"]
             (plus the buffers and button keys through the helpers)
    """
    return (state["x_count"], state["y_count"], False, False)  # TODO
