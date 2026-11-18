# test_input_logic.py  (runs on a laptop)
# Owner: Claire Bryan
# Run from the repo folder with:  python -m unittest discover tests

import unittest
from array import array

import fakes
from fakes import FakeADC, FakePin
import config
import input_handler
import plotter_state


class TestBuffer(unittest.TestCase):

    def test_add_sample_overwrites_one_slot(self):
        buf = array("H", [0] * 8)
        input_handler.add_sample(buf, 3, 1234)
        self.assertEqual(buf[3], 1234)
        self.assertEqual(len(buf), 8)   # never grows

    def test_average(self):
        buf = array("H", [100, 200, 300, 400, 500, 600, 700, 800])
        self.assertEqual(input_handler.average(buf), 450)
        self.assertEqual(input_handler.average(array("H", [65535] * 8)), 65535)


class TestDeadband(unittest.TestCase):

    def test_small_change_is_ignored(self):
        self.assertEqual(input_handler.apply_deadband(1100, 1000), 1000)

    def test_big_change_is_used(self):
        self.assertEqual(input_handler.apply_deadband(1500, 1000), 1500)
        self.assertEqual(input_handler.apply_deadband(500, 1000), 500)


class TestDetectPress(unittest.TestCase):

    def test_new_press(self):
        self.assertTrue(input_handler.detect_press(True, False, 1000, 0))

    def test_held_button_is_not_a_new_press(self):
        self.assertFalse(input_handler.detect_press(True, True, 1000, 0))

    def test_too_soon_after_last_press(self):
        self.assertFalse(input_handler.detect_press(True, False, 1020, 1000))

    def test_button_up(self):
        self.assertFalse(input_handler.detect_press(False, False, 1000, 0))


class TestWithFakeHardware(unittest.TestCase):

    def test_held_button_counts_once(self):
        state = plotter_state.make_state()
        pin = FakePin(0)  # held down the whole time
        presses = 0
        for t in range(1000, 3000, 20):   # 2 s of loops
            if input_handler.check_button(pin, state, "pen", t):
                presses = presses + 1
        self.assertEqual(presses, 1)

    def test_bounce_on_release_is_ignored(self):
        state = plotter_state.make_state()
        pin = FakePin(1)
        levels = [0, 0, 0, 0, 1, 0, 1, 1, 1, 1]   # press, then bouncy release
        presses = 0
        t = 1000
        for level in levels:
            pin.level = level
            if input_handler.check_button(pin, state, "mode", t):
                presses = presses + 1
            t = t + 10
        self.assertEqual(presses, 1)

    def test_twenty_presses(self):
        # like test T2: 20 clean presses, 200 ms apart
        state = plotter_state.make_state()
        pin = FakePin(1)
        presses = 0
        t = 1000
        for i in range(20):
            for level in [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]:
                pin.level = level
                if input_handler.check_button(pin, state, "pen", t):
                    presses = presses + 1
                t = t + 20
        self.assertEqual(presses, 20)

    def test_read_inputs(self):
        state = plotter_state.make_state()
        inputs = input_handler.init_inputs()   # on a laptop: no hardware
        inputs["adc_x"] = FakeADC(40000)
        inputs["adc_y"] = FakeADC(20000)
        inputs["pen_btn"] = FakePin(0)
        inputs["mode_btn"] = FakePin(1)

        result = None
        for loop in range(8):   # fill the 8-sample buffers
            result = input_handler.read_inputs(inputs, state, 1000 + loop * 20)

        self.assertEqual(result[0], 40000)
        self.assertEqual(result[1], 20000)
        self.assertEqual(state["x_count"], 40000)
        self.assertEqual(inputs["index"], 0)   # wrapped 7 -> 0
        self.assertFalse(result[3])            # mode button never pressed


if __name__ == "__main__":
    unittest.main()
