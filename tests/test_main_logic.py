# test_main_logic.py  (runs on a laptop)
# Owner: Abdulelah Aburehla
# Designed and run by: Abdulelah Aburehla
# Runs run_once() from main.py many times with fake knobs, buttons and
# servos, to check that all the files work together before we use the jig.
# Run from the repo folder with:  python -m unittest discover tests

import unittest

import fakes
from fakes import FakeADC, FakePin, FakePWM
import config
import input_handler
import plotter_state
import kinematics
import main
from servo_translator import translate


def fake_setup():
    inputs = input_handler.init_inputs()
    inputs["adc_x"] = FakeADC(32768)
    inputs["adc_y"] = FakeADC(32768)
    inputs["pen_btn"] = FakePin(1)
    inputs["mode_btn"] = FakePin(1)
    servos = {"shoulder": FakePWM(), "elbow": FakePWM(), "pen": FakePWM()}
    state = plotter_state.make_state()
    return inputs, servos, state


class TestWholeLoop(unittest.TestCase):

    def run_loops(self, inputs, servos, state, count, start_ms):
        t = start_ms
        for i in range(count):
            main.run_once(inputs, servos, state, t)
            t = t + config.LOOP_MS
        return t

    def test_joint_mode_follows_the_knobs_slowly(self):
        inputs, servos, state = fake_setup()
        t = self.run_loops(inputs, servos, state, 10, 1000)

        # press the mode button once -> joint mode
        inputs["mode_btn"].level = 0
        t = self.run_loops(inputs, servos, state, 3, t)
        inputs["mode_btn"].level = 1
        t = self.run_loops(inputs, servos, state, 3, t)
        self.assertEqual(state["mode"], config.MODE_JOINT)

        # turn the X knob all the way up
        inputs["adc_x"].value = 65535
        before = state["alpha"]
        self.run_loops(inputs, servos, state, 1, t)
        # one loop never moves a joint more than MAX_STEP_DEG
        self.assertLessEqual(abs(state["alpha"] - before),
                             config.MAX_STEP_DEG + 0.001)

        # after enough loops the shoulder servo reaches the top of its range
        self.run_loops(inputs, servos, state, 100, t + 20)
        self.assertEqual(servos["shoulder"].duty,
                         translate(config.SHOULDER_LIMITS[1]))

    def test_pen_button_lowers_pen(self):
        inputs, servos, state = fake_setup()
        t = self.run_loops(inputs, servos, state, 5, 1000)
        inputs["pen_btn"].level = 0
        t = self.run_loops(inputs, servos, state, 3, t)
        self.assertTrue(state["pen_down"])
        self.assertEqual(servos["pen"].duty,
                         kinematics.clamp(servos["pen"].duty, 0, 65535))

    def test_drawing_mode_keeps_pen_in_safe_area(self):
        inputs, servos, state = fake_setup()
        inputs["adc_x"].value = 65535
        inputs["adc_y"].value = 0
        self.run_loops(inputs, servos, state, 50, 1000)
        self.assertLessEqual(state["x"], config.AREA[0][1])
        self.assertGreaterEqual(state["y"], config.AREA[1][0])


if __name__ == "__main__":
    unittest.main()
