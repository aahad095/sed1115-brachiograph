# test_state.py  (runs on a laptop)
# Owner: Claire Bryan
# Run from the repo folder with:  python -m unittest discover tests

import unittest

import fakes
import config
import plotter_state


class TestState(unittest.TestCase):

    def test_start_values(self):
        state = plotter_state.make_state()
        self.assertFalse(state["pen_down"])
        self.assertEqual(state["mode"], config.MODE_XY)
        self.assertEqual(len(state), 13)

    def test_two_pen_presses_go_back_to_up(self):
        state = plotter_state.make_state()
        plotter_state.update_pen(state, True)
        self.assertTrue(state["pen_down"])
        plotter_state.update_pen(state, True)
        self.assertFalse(state["pen_down"])

    def test_no_press_changes_nothing(self):
        state = plotter_state.make_state()
        plotter_state.update_pen(state, False)
        plotter_state.update_mode(state, False)
        self.assertFalse(state["pen_down"])
        self.assertEqual(state["mode"], config.MODE_XY)

    def test_mode_switch_lifts_pen(self):
        state = plotter_state.make_state()
        state["pen_down"] = True
        plotter_state.update_mode(state, True)
        self.assertEqual(state["mode"], config.MODE_JOINT)
        self.assertFalse(state["pen_down"])
        plotter_state.update_mode(state, True)
        self.assertEqual(state["mode"], config.MODE_XY)

    def test_housekeeping_counts_loops(self):
        state = plotter_state.make_state()
        for i in range(config.DEBUG_EVERY):
            plotter_state.do_housekeeping(state)   # prints one line
        self.assertEqual(state["loop_count"], config.DEBUG_EVERY)


if __name__ == "__main__":
    unittest.main()
