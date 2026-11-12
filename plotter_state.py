# plotter_state.py
# Owner: Claire Bryan
#
# Looks after the "state" dict, which holds everything that changes while
# the program runs (pen position, joint angles, pen up/down, mode).
# The dict is created once and then updated in place, never re-created.
#
# SKELETON ONLY: the headers are final, the code inside is not written yet.

import gc
import config


def make_state():
    """
    Owner:   Claire Bryan
    Purpose: Create the live state dict once, at start-up.
    Inputs:  none (starting values come from config.py)
    Returns: dict "state" with these keys:
               "x", "y"           - float, pen target in mm
               "alpha", "beta"    - float, shoulder and elbow angles in degrees
               "pen_down"         - bool, starts False (pen up)
               "mode"             - int, config.MODE_XY or config.MODE_JOINT
               "x_count", "y_count"             - int, last smoothed knob counts
               "pen_was_down", "mode_was_down"  - bool, button held last loop
               "pen_press_ms", "mode_press_ms"  - int, time of last press
               "loop_count"       - int, number of loops since start-up
    How:     Build the dict with the start values and return it.
    Changes: creates the state dict (the only place it is created)
    """
    state = {
        "x": 0.0,
        "y": 0.0,
        "alpha": config.START_ALPHA,
        "beta": config.START_BETA,
        "pen_down": False,
        "mode": config.MODE_XY,
        "x_count": 0,
        "y_count": 0,
        "pen_was_down": False,
        "mode_was_down": False,
        "pen_press_ms": 0,
        "mode_press_ms": 0,
        "loop_count": 0,
    }
    return state


def update_pen(state, pen_pressed):
    """
    Owner:   Claire Bryan
    Purpose: Flip the pen between up and down when the pen button is pressed.
    Inputs:  state       - the live state dict
             pen_pressed - bool, True if the pen button was pressed this loop
    Returns: nothing
    How:     If pen_pressed is True, set state["pen_down"] to the opposite
             of what it was. Otherwise leave it alone.
    Changes: state["pen_down"]
    """
    pass  # TODO


def update_mode(state, mode_pressed):
    """
    Owner:   Claire Bryan
    Purpose: Switch between drawing mode and joint mode.
    Inputs:  state        - the live state dict
             mode_pressed - bool, True if the mode button was pressed this loop
    Returns: nothing
    How:     If mode_pressed is True, change state["mode"] from MODE_XY to
             MODE_JOINT or back, and lift the pen so switching modes never
             draws a line by accident.
    Changes: state["mode"], state["pen_down"]
    """
    pass  # TODO


def do_housekeeping(state):
    """
    Owner:   Claire Bryan
    Purpose: Do the slow jobs that don't need to run every loop.
    Inputs:  state - the live state dict
    Returns: nothing
    How:     Add 1 to state["loop_count"]. Every config.DEBUG_EVERY loops,
             print the state on one line for Thonny. Every config.GC_EVERY
             loops, call gc.collect() so garbage collection happens at a
             time we choose.
    Changes: state["loop_count"]
    """
    pass  # TODO
