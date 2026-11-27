# pico_test_inputs.py  (tests T1 and T2, runs on the PICO)
# Owner: Claire Bryan
# Designed and run by: Claire Bryan
#
# Upload this file to the Pico next to the project files, open it in Thonny
# and press Run. No servos move in this test.
#
# T1: turn each knob end to end. The lowest and highest counts seen are
#     printed. Pass: both knobs cover at least 95% of 0-65535, and the
#     number stays within 200 counts when you let go.
# T2: press each button 20 times, then hold it for 2 s.
#     Pass: exactly 20 presses counted, and holding counts as one press.
# Press Stop in Thonny to end the test.

import time
import input_handler
import plotter_state

inputs = input_handler.init_inputs()
state = plotter_state.make_state()

lowest_x = 65535
highest_x = 0
lowest_y = 65535
highest_y = 0
pen_presses = 0
mode_presses = 0
loops = 0

print("Turn the knobs end to end and press the buttons. Stop to finish.")
while True:
    now = time.ticks_ms()
    x, y, pen, mode = input_handler.read_inputs(inputs, state, now)

    lowest_x = min(lowest_x, x)
    highest_x = max(highest_x, x)
    lowest_y = min(lowest_y, y)
    highest_y = max(highest_y, y)
    if pen:
        pen_presses = pen_presses + 1
        print("pen press", pen_presses)
    if mode:
        mode_presses = mode_presses + 1
        print("mode press", mode_presses)

    loops = loops + 1
    if loops % 25 == 0:
        print("x", x, "(", lowest_x, "-", highest_x, ")",
              " y", y, "(", lowest_y, "-", highest_y, ")",
              " x covers %d%%" % ((highest_x - lowest_x) * 100 // 65535),
              " y covers %d%%" % ((highest_y - lowest_y) * 100 // 65535))
    time.sleep_ms(20)
