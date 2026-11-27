# lab7_skeleton.py
# SED 1115 - Lab 7: Plotter Control
# Skeleton "calling structure" code to review with the TA before writing the functions.
# Only the function headers and the data structures are here, no code inside yet.
#
#   G-Code file -> G-Code parser -> command interpreter -> servo translator -> servos
#                                                       -> other commands (pen up/down, disable)

# ---- Data structures ----
# servos: dictionary of the three PWM outputs
#     {"shoulder": PWM(Pin(0)), "elbow": PWM(Pin(1)), "wrist": PWM(Pin(2))}
# one parsed line of G-Code: a command string and a dictionary of parameters
#     "G1 S62.858 E54.284"  ->  ("G1", {"S": 62.858, "E": 54.284})
#     "M3"                  ->  ("M3", {})


# ---- G-Code parser (gcode_parser.py) ----
def parse_line(line):
    """Returns (command, params) for one line of G-Code, or (None, {}) for a blank line."""
    pass


# ---- Servo translator (servo_translator.py from Lab 6) ----
def translate(angle):
    """Converts an angle in degrees to a safe duty_u16 value."""
    pass


# ---- Servo functions ----
def setup_servos():
    """Creates the three servo PWM outputs at 50 Hz and returns the servos dictionary."""
    pass


def move_servo(servo, angle):
    """Moves one servo to an angle using translate()."""
    pass


# ---- Other commands ----
def move_arm(servos, params):
    """G1: moves the shoulder (S) and/or elbow (E) servo."""
    pass


def pen_down(servos):
    """M3: wrist servo to the down position (about 30 degrees)."""
    pass


def pen_up(servos):
    """M5: wrist servo to the up position (0 degrees)."""
    pass


def disable_servos(servos):
    """M18: turns off the PWM signal to all servos."""
    pass


# ---- Command interpreter ----
def run_command(command, params, servos):
    """Calls the right function for G1, M3, M5 or M18."""
    pass


# ---- G-Code file ----
def run_gcode_file(filename, servos):
    """Opens the file, parses each line and runs each command."""
    pass


def main():
    """Sets up the servos, lifts the pen and draws the G-Code file."""
    pass
