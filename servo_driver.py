# servo_driver.py
# Owner: Abdulelah Aburehla
#
# The only file that is allowed to move a servo. Every angle is corrected
# with its calibration offset and clamped to the servo limits here, and the
# arm servos are moved through the safety function the course gave us.

import config
from kinematics import clamp

# REUSED CODE: translate() is the safe angle-to-duty function given to us by
# the course in Lab 6 (servo_translator.py, not written by us). It clamps
# the angle to 0-180 degrees and turns it into a duty_u16() value
# (1638 = 0.5 ms pulse, 8192 = 2.5 ms pulse). Every servo command in this
# file goes through it.
from servo_translator import translate

# "machine" only exists on the Pico. On a laptop we set it to None so the
# functions that don't touch hardware can still be unit tested.
try:
    import machine
except ImportError:
    machine = None


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
    servos = {
        "shoulder": machine.PWM(machine.Pin(config.PIN_SHOULDER)),
        "elbow": machine.PWM(machine.Pin(config.PIN_ELBOW)),
        "pen": machine.PWM(machine.Pin(config.PIN_PEN)),
    }
    for name in servos:
        servos[name].freq(config.PWM_FREQ)
    return servos


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
    servo_angle = joint_angle + offset
    return clamp(servo_angle, limits[0], limits[1])


def angle_to_duty(angle):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Turn a servo angle into a PWM duty value (used for the pen servo).
    Inputs:  angle - float, 0 to 180 degrees
    Returns: int, value for duty_u16() (0-65535)
    How:     Scale 0-180 degrees onto 0.5 ms to 2.5 ms of a 20 ms period.
             This is exactly what the provided translate() does, so we
             just call it instead of writing the scaling again.
    Changes: nothing
    """
    return translate(angle)


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
    shoulder = joint_to_servo_angle(alpha, config.SHOULDER_OFFSET,
                                    config.SHOULDER_LIMITS)
    elbow = joint_to_servo_angle(beta, config.ELBOW_OFFSET,
                                 config.ELBOW_LIMITS)
    servos["shoulder"].duty_u16(translate(shoulder))
    servos["elbow"].duty_u16(translate(elbow))


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
    if pen_down:
        angle = config.PEN_DOWN
    else:
        angle = config.PEN_UP
    servos["pen"].duty_u16(angle_to_duty(angle))


def stop_servos(servos):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Let all three servos go limp when the program stops.
    Inputs:  servos - dict from init_servos()
    Returns: nothing
    How:     Write a duty of 0 to every servo (same as M18 in Lab 7).
    Changes: all three PWM outputs
    """
    for name in servos:
        servos[name].duty_u16(0)
