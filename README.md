# sed1115-brachiograph

SED1115 Group 1 (Abdulelah Aburehla, Abdul Ahad, Claire Bryan) – MicroPython code for a Raspberry Pi Pico that controls a BrachioGraph pen plotter like an Etch a Sketch. Two knobs move the pen, one button lifts or drops the pen, and a second button switches between drawing mode and joint mode.

## What you need

- Raspberry Pi Pico with **MicroPython v1.29.0** (RPI_PICO build) – from micropython.org
- **Thonny 4.x** with the "MicroPython (Raspberry Pi Pico)" interpreter selected
- The lab accessory board (two knobs, two buttons) and the plotter jig
- Only for the laptop tests: **Python 3.12** (any Python 3 works)

**No libraries to install.** Everything we use (`machine`, `time`, `math`, `array`, `gc`, `micropython.const`) is built into the MicroPython firmware, and the laptop tests only use Python's built-in `unittest`.

## Wiring

| What | Pico pin |
|---|---|
| X knob | GP26 (ADC0) |
| Y knob | GP27 (ADC1) |
| Pen button | GP10 (pull-up, pressed = 0) – to be confirmed, issue #39 |
| Mode button | GP11 (pull-up, pressed = 0) – to be confirmed, issue #39 |
| Shoulder servo | GP0 (J1) |
| Elbow servo | GP1 (J2) |
| Pen servo | GP2 (J3) |

Change any of these in `config.py`.

## How to run it on the Pico

1. In Thonny, open the Files tab and upload these 7 files to the root of the Pico (right-click → **Upload to /**):
   `main.py`, `config.py`, `input_handler.py`, `plotter_state.py`, `kinematics.py`, `servo_driver.py`, `servo_translator.py`
2. Press Run on `main.py`, or unplug and plug the Pico back in (`main.py` starts by itself).
3. The pen starts **up**, in **drawing mode**. Turn the knobs to move the pen, press the pen button to put it down.
4. Press the mode button for **joint mode** (X knob = shoulder, Y knob = elbow). The pen lifts every time the mode changes.
5. Twice a second the shell prints a line like
   `mode: draw | knobs: 31890 40211 | x,y mm: 108.7 152.5 | alpha,beta: 153.8 118.2 | pen down: False`
   (alpha and beta are the arm's joint angles from the maths, not the servo angles)
6. Press Stop in Thonny to end. The pen lifts and the servos go limp.

In drawing mode the knobs cover the safe area x 60–160 mm, y 85–195 mm (measured from the bottom-left of the paper). The servo limits in `config.py` are the safe ranges from the Lab 7 G-code files, so the arm can't leave them in either mode.

## Calibration (joint angle → servo angle)

```
shoulder servo = alpha - 75
elbow servo    = 150 - beta
```

We worked these out from the Lab 7 G-code files, which the course made for this jig. With these numbers `square.gcode` is exactly a 100 mm square (x 58–158, y 89.5–189.5), `line.gcode` a 100 mm line and `circle.gcode` a 50 mm radius circle. `tests/test_kinematics.py` checks that our `solve()` gives the same servo angles as `square.gcode` at all four corners (within 0.1°). They are stored in `config.py` as `SHOULDER_OFFSET`, `SHOULDER_DIR`, `ELBOW_OFFSET` and `ELBOW_DIR`.

## How to run the tests

Laptop tests (no Pico needed), from the repo folder:

```
python -m unittest discover tests
```

All 46 should pass. They cover every function that doesn't need hardware, the calibration against the Lab 7 G-code, plus fake-hardware checks of the buttons, servos and the whole loop.

On-Pico tests: upload the project files plus the test file, then Run it in Thonny.

| File | Test | What to do |
|---|---|---|
| `tests/pico_test_inputs.py` | T1, T2 | Turn each knob end to end, press each button 20 times, hold it 2 s |
| `tests/pico_test_servos.py` | T3, T5 | Watch the arm sweep each joint and the pen go down/up 10 times |

## Files

| File | Owner | What it does |
|---|---|---|
| `main.py` | Abdulelah | Set-up and the 20 ms loop |
| `config.py` | Abdulelah | Pins, timing, geometry, servo limits, safe area |
| `input_handler.py` | Claire | Knob smoothing (8-sample average + deadband), button debounce |
| `plotter_state.py` | Claire | The state dict, pen/mode toggling, debug print, garbage collection |
| `kinematics.py` | Abdul Ahad | Knob counts → mm → shoulder and elbow angles, smoothing |
| `servo_driver.py` | Abdulelah | Offsets, limits and PWM output for the three servos |
| `servo_translator.py` | **course material** | `translate()`: safe angle → duty_u16 (see below) |
| `tests/` | all | Laptop unit tests and on-Pico tests (owner of each is in its header) |
| `lab7/` | all | Our Lab 7 G-code plotter, kept for reference. Not part of the project. |

## Reused code and credits

- **`servo_translator.py` is NOT our code.** It is the `translate()` function given to us by the SED1115 teaching team in Lab 6. We use it unchanged as the safety function for every servo command (it clamps the angle to 0–180° and returns a duty value between 0.5 ms and 2.5 ms).
- **MicroPython** (MIT License, github.com/micropython/micropython) – the firmware and its built-in modules.
- **BrachioGraph** by D. Procida (MIT License, github.com/evildmp/BrachioGraph) – we used the idea of solving the arm angles with the law of cosines. No code was copied; the formulas are from our project brief.
- All other files were written by our group, with help from generative AI (Claude, by Anthropic), which our course allows. See our Deliverable C report for details.

## Status

Orange: the code is complete and passes all laptop tests, and the demo runs. Still open (see the Issues tab): the on-jig tests T1–T3 and T5–T8, confirming the button pins, and checking that the paper covers the safe area.

Every file has a header saying who designed it and who tested it.

Our own code is under the MIT License (see LICENSE).
