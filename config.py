# config.py
# Owner: Abdulelah Aburehla
#
# All the fixed numbers for the project live in this one file.
# There are no functions here. Every other file imports this one.
# Nothing in this file changes while the program is running.
#
# Designed by: Abdulelah Aburehla
# Tested by:   Abdulelah Aburehla (tests/test_servo_logic.py),
#              Abdul Ahad (calibration numbers, tests/test_kinematics.py)
#
# The servo limits, pen angles and button pins still need a final check
# on the jig. Each one has its own GitHub issue.

# const() only exists in MicroPython. On a laptop we use a stand-in
# so the unit tests can still import this file.
try:
    from micropython import const
except ImportError:
    def const(value):
        return value

# ---- Pins (servo pins match Lab 7: J1, J2, J3. Button pins: TODO confirm, issue #39) ----
PIN_KNOB_X = const(26)      # ADC0, X potentiometer
PIN_KNOB_Y = const(27)      # ADC1, Y potentiometer
PIN_PEN_BUTTON = const(10)  # push button, pulled up (pressed = 0)
PIN_MODE_BUTTON = const(11) # push button, pulled up (pressed = 0)
PIN_SHOULDER = const(0)     # PWM, shoulder servo
PIN_ELBOW = const(1)        # PWM, elbow servo
PIN_PEN = const(2)          # PWM, pen servo

# ---- Timing ----
LOOP_MS = const(20)         # one loop every 20 ms (matches 50 Hz servos)
DEBOUNCE_MS = const(50)     # ignore button changes closer than this
DEBUG_EVERY = const(25)     # print the state every 25 loops (0.5 s)
GC_EVERY = const(50)        # run gc.collect() every 50 loops (1 s)
PWM_FREQ = const(50)        # servo PWM frequency in Hz

# ---- Modes ----
MODE_XY = const(0)          # drawing mode: knobs move the pen in x and y
MODE_JOINT = const(1)       # joint mode: knobs move the servos directly

# ---- Knob smoothing ----
BUFFER_SIZE = const(8)      # number of samples in the moving average
DEADBAND = const(200)       # ignore knob changes smaller than this (counts)
MAX_COUNT = const(65535)    # largest value read_u16() can return

# ---- Arm geometry in mm (from the project brief) ----
SHOULDER = (-50.0, 139.5)   # shoulder pivot (x, y) from bottom-left of paper
LA = 155.0                  # shoulder-to-elbow link length
LB = 155.0                  # elbow-to-pen link length

# ---- Safe drawing area in mm: ((x_min, x_max), (y_min, y_max)) ----
# The biggest rectangle where every point needs servo angles at least
# 0.5 degrees inside SHOULDER_LIMITS and ELBOW_LIMITS (checked every 2.5 mm,
# see test_kinematics.py). It contains the 100 mm square from Lab 7.
# Still to check on the jig that the paper covers it (issue #35).
AREA = ((60.0, 160.0), (85.0, 195.0))

# ---- Servo limits in degrees: (min, max) ----
# For now these are the angle ranges the Lab 7 G-code files used on the jig
# (shoulder 47.8-107.3, elbow 10.8-57.3), rounded out a little. We know the
# arm is safe inside them. They get replaced by measured values in task 3
# (issue #34).
SHOULDER_LIMITS = (45.0, 110.0)
ELBOW_LIMITS = (10.0, 60.0)

# ---- Joint angle -> servo angle ----
# servo angle = OFFSET + DIR * joint angle
#   shoulder servo = alpha - 75
#   elbow servo    = 150 - beta   (the elbow servo turns the opposite way)
# Worked out from the Lab 7 G-code files, which were made for this jig:
# with these numbers line.gcode is a 100 mm line, square.gcode a 100 mm
# square and circle.gcode a 50 mm radius circle (issue #36).
SHOULDER_OFFSET = -75.0
SHOULDER_DIR = 1
ELBOW_OFFSET = 150.0
ELBOW_DIR = -1

# ---- Pen servo positions in degrees ----
PEN_UP = 0.0                     # from the Lab 7 handout
PEN_DOWN = 30.0                  # from the Lab 7 handout

# ---- Smoothing ----
MAX_STEP_DEG = 2.0               # most a joint may move in one loop (degrees)

# ---- Where the arm starts: joint angles for the middle of AREA (110, 140) ----
# (servo angles 74.1 and 32.1, inside the limits above)
START_ALPHA = 149.1
START_BETA = 117.9
