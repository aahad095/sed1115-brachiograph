# kinematics.py
# Owner: Abdul Ahad
#
# All the maths: turns knob counts into a point on the paper, keeps that
# point inside the safe area, and works out the shoulder and elbow angles.
# This file uses no hardware, so it runs the same on a laptop for testing.
#
# SKELETON ONLY: the headers are final, the code inside is not written yet.
# Each function returns a placeholder so the whole program can be imported.

import math
import config


def clamp(value, low, high):
    """
    Owner:   Abdul Ahad
    Purpose: Keep a number between two limits.
    Inputs:  value - float or int, the number to check
             low   - the smallest value allowed
             high  - the largest value allowed
    Returns: value if it is inside the limits, otherwise low or high
    How:     If value < low return low. If value > high return high.
             Otherwise return value. (servo_driver.py reuses this.)
    Changes: nothing
    """
    return value  # TODO


def count_to_mm(count, low_mm, high_mm):
    """
    Owner:   Abdul Ahad
    Purpose: Turn one knob count into a distance along one axis.
    Inputs:  count   - int 0-65535 from the knob
             low_mm  - float, position in mm when the knob is fully down
             high_mm - float, position in mm when the knob is fully up
    Returns: float, position in mm between low_mm and high_mm
    How:     Straight-line scaling:
             low_mm + (count / config.MAX_COUNT) * (high_mm - low_mm)
    Changes: nothing
    """
    return low_mm  # TODO


def count_to_angle(count, min_deg, max_deg):
    """
    Owner:   Abdul Ahad
    Purpose: Turn one knob count straight into a joint angle (joint mode).
    Inputs:  count   - int 0-65535 from the knob
             min_deg - float, angle when the knob is fully down
             max_deg - float, angle when the knob is fully up
    Returns: float, angle in degrees between min_deg and max_deg
    How:     Same straight-line scaling as count_to_mm(), but in degrees.
    Changes: nothing
    """
    return min_deg  # TODO


def to_mm(x_count, y_count):
    """
    Owner:   Abdul Ahad
    Purpose: Turn both knob counts into a pen position on the paper.
    Inputs:  x_count, y_count - int 0-65535, smoothed knob counts
    Returns: tuple (x, y), floats in mm from the bottom-left of the paper
    How:     Call count_to_mm() once for x and once for y, using the limits
             stored in config.AREA.
    Changes: nothing
    """
    return (0.0, 0.0)  # TODO


def clamp_to_area(x, y):
    """
    Owner:   Abdul Ahad
    Purpose: Make sure the pen target never leaves the safe drawing area.
    Inputs:  x, y - float, pen target in mm
    Returns: tuple (x, y), floats in mm, moved to the edge if they were outside
    How:     Call clamp() on x with the x limits and on y with the y limits
             from config.AREA.
    Changes: nothing
    """
    return (x, y)  # TODO


def distance_from_shoulder(x, y):
    """
    Owner:   Abdul Ahad
    Purpose: Find how far the pen target is from the shoulder pivot.
    Inputs:  x, y - float, pen target in mm
    Returns: float d, distance in mm
    How:     Pythagoras using config.SHOULDER:
             d = sqrt((x + 50)^2 + (y - 139.5)^2)
    Changes: nothing
    """
    return 0.0  # TODO


def elbow_angle(d):
    """
    Owner:   Abdul Ahad
    Purpose: Work out the elbow angle (beta) for a given reach.
    Inputs:  d - float, shoulder-to-pen distance in mm
    Returns: float beta, in degrees
    How:     Law of cosines:
             beta = 180 - acos((LA^2 + LB^2 - d^2) / (2 * LA * LB))
             then convert from radians to degrees.
    Changes: nothing
    """
    return 0.0  # TODO


def shoulder_angle(x, y, d):
    """
    Owner:   Abdul Ahad
    Purpose: Work out the shoulder angle (alpha) for a pen target.
    Inputs:  x, y - float, pen target in mm
             d    - float, shoulder-to-pen distance in mm
    Returns: float alpha, in degrees
    How:     alpha = 90 + atan2(y - 139.5, x + 50)
                        + acos((LA^2 + d^2 - LB^2) / (2 * LA * d))
             with both parts converted from radians to degrees.
    Changes: nothing
    """
    return 0.0  # TODO


def solve(x, y):
    """
    Owner:   Abdul Ahad
    Purpose: Turn a pen position into the two joint angles.
    Inputs:  x, y - float, pen target in mm
    Returns: tuple (alpha, beta) in degrees, or None if the arm can't reach
    How:     Call distance_from_shoulder(). If d is 0 or bigger than LA + LB,
             return None. Otherwise call shoulder_angle() and elbow_angle()
             and return both.
    Changes: nothing
    """
    return (config.START_ALPHA, config.START_BETA)  # TODO


def limit_step(old, new, max_step):
    """
    Owner:   Abdul Ahad
    Purpose: Stop a joint from jumping too far in one loop (smoothing).
    Inputs:  old      - float, the angle sent last loop (degrees)
             new      - float, the angle we want now (degrees)
             max_step - float, the biggest change allowed in one loop
    Returns: float, an angle no more than max_step away from old
    How:     If new is within max_step of old, return new. Otherwise return
             old plus or minus max_step, moving towards new.
    Changes: nothing
    """
    return new  # TODO


def get_target_angles(state, x_count, y_count):
    """
    Owner:   Abdul Ahad
    Purpose: Decide which joint angles the knobs are asking for, in either mode.
    Inputs:  state            - the live state dict
             x_count, y_count - int 0-65535, smoothed knob counts
    Returns: tuple (alpha, beta), floats in degrees
    How:     Joint mode: call count_to_angle() for each knob with the servo
             limits from config. Drawing mode: call to_mm(), clamp_to_area()
             and solve(). If solve() returns None, keep the angles already
             in the state so the arm just holds still.
    Changes: state["x"], state["y"] (drawing mode only)
    """
    return (state["alpha"], state["beta"])  # TODO
