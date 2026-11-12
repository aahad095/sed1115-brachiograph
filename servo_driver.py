# servo_driver.py
# Owner: Abdulelah Aburehla
#
# The only file that is allowed to move a servo. Every angle is corrected
# with its calibration offset and clamped to the servo limits here, and the
# arm servos are moved through the safety function the course gave us.
#
# SKELETON ONLY: the headers are final, the code inside is not written yet.
# Each function returns a placeholder so the whole program can be imported.

import config
from kinematics import clamp

# "machine" only exists on the Pico. On a laptop we set it to None so the
# functions that don't touch hardware can still be unit tested.
try:
    import machine
except ImportError:
    machine = None

# TODO: import the safety function provided on BrightSpace here once we
# have read and tested it (Deliverable A, task 3). Until then move_arm()
# only describes how it will be called.


def init_servos():
    """
    Owner:   Abdulelah Aburehla
    Purpose: Set up the three servo outputs once, at start-up.
    Inputs:  none (pin numbers and frequency come from config.py)
    Returns: dict "servos" with keys "shoulder", "elbow" and "pen",
             each a machine.PWM object running at 50 Hz
    How:     Create a PWM object on each servo pin, set its frequency to
             config.PWM_FREQ, and put the three objects in one dict.
    Changes: creates the servos dict (the only place it is created)
    """
    servos = {"shoulder": None, "elbow": None, "pen": None}
    return servos  # TODO: create the real PWM objects


def joint_to_servo_angle(joint_angle, offset, limits):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Turn a joint angle from the maths into an angle the servo can use.
    Inputs:  joint_angle - float, alpha or beta in degrees
             offset      - float, calibration offset in degrees (from config)
             limits      - tuple (min, max) in degrees (from config)
    Returns: float, servo angle in degrees, always inside the limits
    How:     Add the offset, then call clamp() with the limits.
    Changes: nothing
    """
    return joint_angle  # TODO


def angle_to_duty(angle):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Turn a servo angle into a PWM duty value (used for the pen servo).
    Inputs:  angle - float, 0 to 180 degrees
    Returns: int, value for duty_u16() (0-65535)
    How:     Scale 0-180 degrees onto the pulse widths measured during
             calibration (about 0.5 ms to 2.5 ms of a 20 ms period).
    Changes: nothing
    """
    return 0  # TODO


def move_arm(servos, alpha, beta):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Move the shoulder and elbow servos to new joint angles, safely.
    Inputs:  servos - dict from init_servos()
             alpha  - float, shoulder joint angle in degrees
             beta   - float, elbow joint angle in degrees
    Returns: nothing
    How:     Call joint_to_servo_angle() for each joint with its offset and
             limits from config, then pass both servo angles to the provided
             safety function, which sets the PWM outputs.
    Changes: the shoulder and elbow PWM outputs
    """
    pass  # TODO


def set_pen(servos, pen_down):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Raise or lower the pen.
    Inputs:  servos   - dict from init_servos()
             pen_down - bool, True to lower the pen, False to raise it
    Returns: nothing
    How:     Pick config.PEN_DOWN or config.PEN_UP, call angle_to_duty(),
             and write the result to the pen servo with duty_u16().
    Changes: the pen PWM output
    """
    pass  # TODO
