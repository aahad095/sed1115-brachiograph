# main.py
# SED 1115 - Lab 7: Plotter Control
# Reads a G-Code file and draws the shape on the pen plotter jig.
#
# Files that need to be uploaded to the Pico:
#   main.py, gcode_parser.py, servo_translator.py and the .gcode file(s)
#
# Calling structure:
#   G-Code file -> parse_line() -> run_command() -> move_servo() -> translate() -> servos
#                                               -> pen_up() / pen_down() / disable_servos()

from machine import Pin, PWM
import time

from servo_translator import translate
from gcode_parser import parse_line

# ---------------- Settings ----------------

# Change this to draw a different shape:
# "line.gcode", "square.gcode", "circle.gcode" or "circle_and_square.gcode"
GCODE_FILE = "circle.gcode"

# Servo connectors on the expansion board: J1 = GPIO 0, J2 = GPIO 1, J3 = GPIO 2
SHOULDER_PIN = 0
ELBOW_PIN = 1
WRIST_PIN = 2

# Small angle corrections for our jig. Start at 0 and adjust after testing.
SHOULDER_OFFSET = 0
ELBOW_OFFSET = 0

# Wrist (pen) angles from the lab handout: 0 = up, about 30 = down
PEN_UP_ANGLE = 0
PEN_DOWN_ANGLE = 30

# Waiting times in seconds so the servos can finish moving
MOVE_DELAY = 0.05     # after each small G1 move
PEN_DELAY = 0.3       # after the pen goes up or down
SETTLE_DELAY = 0.5    # before the pen goes down, so the arm has finished travelling


# ---------------- Servo functions ----------------

def setup_servos():
    """Creates the three servo PWM outputs at 50 Hz and returns them in a dictionary."""
    servos = {
        "shoulder": PWM(Pin(SHOULDER_PIN)),
        "elbow": PWM(Pin(ELBOW_PIN)),
        "wrist": PWM(Pin(WRIST_PIN)),
    }
    for name in servos:
        servos[name].freq(50)
    return servos


def move_servo(servo, angle):
    """Moves one servo. translate() turns the angle into a safe duty_u16 value."""
    servo.duty_u16(translate(angle))


def move_arm(servos, params):
    """G1: moves the shoulder and/or the elbow. Only the ones in params are moved."""
    if "S" in params:
        move_servo(servos["shoulder"], params["S"] + SHOULDER_OFFSET)
    if "E" in params:
        move_servo(servos["elbow"], params["E"] + ELBOW_OFFSET)
    time.sleep(MOVE_DELAY)


def pen_down(servos):
    """M3: puts the pen down on the paper."""
    time.sleep(SETTLE_DELAY)
    move_servo(servos["wrist"], PEN_DOWN_ANGLE)
    time.sleep(PEN_DELAY)


def pen_up(servos):
    """M5: lifts the pen off the paper."""
    move_servo(servos["wrist"], PEN_UP_ANGLE)
    time.sleep(PEN_DELAY)


def disable_servos(servos):
    """M18: stops the PWM signal to all three servos so they go limp."""
    for name in servos:
        servos[name].duty_u16(0)


# ---------------- Command interpreter ----------------

def run_command(command, params, servos):
    """Checks which command it is and calls the right function."""
    if command == "G1":
        move_arm(servos, params)
    elif command == "M3":
        pen_down(servos)
    elif command == "M5":
        pen_up(servos)
    elif command == "M18":
        disable_servos(servos)
    else:
        print("Unknown command, skipped:", command)


# ---------------- G-Code file ----------------

def run_gcode_file(filename, servos):
    """Reads the G-Code file one line at a time and runs each command."""
    with open(filename, "r") as f:
        for line in f:
            command, params = parse_line(line)
            if command is not None:
                print(command, params)
                run_command(command, params, servos)


def main():
    servos = setup_servos()
    pen_up(servos)   # always start with the pen up
    try:
        run_gcode_file(GCODE_FILE, servos)
        print("Done drawing", GCODE_FILE)
    except OSError:
        print("Could not open", GCODE_FILE, "- did you upload it to the Pico?")
    finally:
        # this still runs if we press Stop in Thonny, so the pen never stays down
        pen_up(servos)
        disable_servos(servos)


if __name__ == "__main__":
    main()
