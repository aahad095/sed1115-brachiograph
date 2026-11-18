# test_servo_logic.py  (runs on a laptop)
# Owner: Abdulelah Aburehla
# Run from the repo folder with:  python -m unittest discover tests

import unittest

import fakes
from fakes import FakePWM
import config
import servo_driver
from servo_translator import translate


class TestServoLogic(unittest.TestCase):

    def test_offset_is_added(self):
        self.assertEqual(servo_driver.joint_to_servo_angle(70, 5, (45, 110)), 75)

    def test_past_a_limit_comes_back_as_the_limit(self):
        self.assertEqual(servo_driver.joint_to_servo_angle(120, 0, (45, 110)), 110)
        self.assertEqual(servo_driver.joint_to_servo_angle(35, 0, (45, 110)), 45)

    def test_angle_to_duty(self):
        self.assertEqual(servo_driver.angle_to_duty(0), 1638)     # 0.5 ms
        self.assertEqual(servo_driver.angle_to_duty(180), 8192)   # 2.5 ms
        self.assertEqual(servo_driver.angle_to_duty(90), 4915)

    def test_move_arm_never_leaves_the_limits(self):
        servos = {"shoulder": FakePWM(), "elbow": FakePWM(), "pen": FakePWM()}
        servo_driver.move_arm(servos, 999, -999)
        self.assertEqual(servos["shoulder"].duty,
                         translate(config.SHOULDER_LIMITS[1]))
        self.assertEqual(servos["elbow"].duty,
                         translate(config.ELBOW_LIMITS[0]))

    def test_set_pen(self):
        servos = {"shoulder": FakePWM(), "elbow": FakePWM(), "pen": FakePWM()}
        servo_driver.set_pen(servos, True)
        self.assertEqual(servos["pen"].duty, translate(config.PEN_DOWN))
        servo_driver.set_pen(servos, False)
        self.assertEqual(servos["pen"].duty, translate(config.PEN_UP))

    def test_stop_servos(self):
        servos = {"shoulder": FakePWM(), "elbow": FakePWM(), "pen": FakePWM()}
        servo_driver.stop_servos(servos)
        self.assertEqual(servos["pen"].duty, 0)


if __name__ == "__main__":
    unittest.main()
