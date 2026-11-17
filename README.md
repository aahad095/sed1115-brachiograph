# SED 1115 – Lab 7: Plotter Control

MicroPython program for the Raspberry Pi Pico that reads a G-Code file and draws the shape on the pen plotter jig.

## Files

| File | What it does |
|---|---|
| `main.py` | Sets up the servos, reads the G-Code file and runs each command (command interpreter + servo functions) |
| `gcode_parser.py` | `parse_line()` turns one line of G-Code into a command and a dictionary of parameters |
| `servo_translator.py` | `translate()` from Lab 6: converts an angle to a safe `duty_u16` value |
| `test_lab7.py` | Unit tests for `parse_line()`, `translate()` and the G-Code files (does not move the servos) |
| `lab7_skeleton.py` | The skeleton "calling structure" code (function headers only) reviewed with the TA |
| `line.gcode`, `square.gcode`, `circle.gcode`, `circle_and_square.gcode` | Shapes to draw |

## Calling structure

```
G-Code file -> parse_line() -> run_command() -> move_servo() -> translate() -> servos
                                             -> pen_up() / pen_down() / disable_servos()
```

## Supported G-Code

| Command | Action |
|---|---|
| `G1 S<angle> E<angle>` | Move the shoulder (S) and/or elbow (E) servo. Only the ones given are moved. |
| `M3` | Pen down (wrist servo to 30°) |
| `M5` | Pen up (wrist servo to 0°) |
| `M18` | Disable all servos |

Blank lines and comments (anything after `;`) are ignored. Unknown commands are printed and skipped.

## How to run

1. Upload `main.py`, `gcode_parser.py`, `servo_translator.py` and the `.gcode` files to the Pico (Thonny: Files tab → right-click → **Upload to /**).
2. In `main.py`, set `GCODE_FILE` to the shape you want, e.g. `GCODE_FILE = "square.gcode"`.
3. Run `main.py`. Each command is printed in the shell as it runs.
4. If the drawing is shifted, adjust `SHOULDER_OFFSET` and `ELBOW_OFFSET` at the top of `main.py` a few degrees at a time.

Servo connectors: J1 (GPIO 0) = shoulder, J2 (GPIO 1) = elbow, J3 (GPIO 2) = wrist.

## Tests

Run `test_lab7.py` on the Pico or on a laptop. It checks the parser, the translator (including clamping below 0° and above 180°), and that every uploaded G-Code file only uses known commands with angles between 0 and 180.
