# test_kinematics.py  (test T4, runs on a laptop)
# Owner: Abdul Ahad
# Run from the repo folder with:  python -m unittest discover tests

import math
import unittest

import fakes  # sets up the import path
import config
import kinematics


def pen_position(alpha, beta):
    """
    Forward kinematics, used only to check solve(). Starts at the shoulder,
    goes along link A, then along link B, and returns where the pen ends up.
    If solve() is right, this lands back on the point we asked for.
    """
    a = math.radians(alpha - 90)          # direction of link A
    b = math.radians(alpha - 90 - beta)   # direction of link B
    ex = config.SHOULDER[0] + config.LA * math.cos(a)
    ey = config.SHOULDER[1] + config.LA * math.sin(a)
    return (ex + config.LB * math.cos(b), ey + config.LB * math.sin(b))


class TestSmallHelpers(unittest.TestCase):

    def test_clamp(self):
        self.assertEqual(kinematics.clamp(5, 0, 10), 5)
        self.assertEqual(kinematics.clamp(-3, 0, 10), 0)
        self.assertEqual(kinematics.clamp(15, 0, 10), 10)
        self.assertEqual(kinematics.clamp(10, 0, 10), 10)

    def test_count_to_mm(self):
        self.assertAlmostEqual(kinematics.count_to_mm(0, 20, 190), 20)
        self.assertAlmostEqual(kinematics.count_to_mm(65535, 20, 190), 190)
        self.assertAlmostEqual(kinematics.count_to_mm(32767.5, 20, 190), 105)

    def test_count_to_angle(self):
        self.assertAlmostEqual(kinematics.count_to_angle(0, 45, 110), 45)
        self.assertAlmostEqual(kinematics.count_to_angle(65535, 45, 110), 110)

    def test_to_mm_uses_area(self):
        x, y = kinematics.to_mm(0, 65535)
        self.assertAlmostEqual(x, config.AREA[0][0])
        self.assertAlmostEqual(y, config.AREA[1][1])

    def test_clamp_to_area(self):
        self.assertEqual(kinematics.clamp_to_area(100, 100), (100, 100))
        x, y = kinematics.clamp_to_area(-500, 999)
        self.assertEqual(x, config.AREA[0][0])
        self.assertEqual(y, config.AREA[1][1])

    def test_distance_from_shoulder(self):
        # 3-4-5 triangle measured from the shoulder (-50, 139.5)
        self.assertAlmostEqual(
            kinematics.distance_from_shoulder(-50 + 30, 139.5 + 40), 50)

    def test_elbow_angle_straight_arm(self):
        # arm fully stretched out: the elbow is straight, so beta = 0
        self.assertAlmostEqual(kinematics.elbow_angle(310), 0, places=3)

    def test_limit_step(self):
        self.assertEqual(kinematics.limit_step(90, 91, 2), 91)
        self.assertEqual(kinematics.limit_step(90, 100, 2), 92)
        self.assertEqual(kinematics.limit_step(90, 80, 2), 88)


class TestSolve(unittest.TestCase):

    def test_brief_example(self):
        # worked example from the project brief: (139.4, 73) -> 120.3, 99.3
        d = kinematics.distance_from_shoulder(139.4, 73.0)
        self.assertAlmostEqual(d, 200.7, delta=0.1)
        alpha, beta = kinematics.solve(139.4, 73.0)
        self.assertAlmostEqual(alpha, 120.3, delta=0.5)
        self.assertAlmostEqual(beta, 99.3, delta=0.5)

    def test_safe_area_corners_and_centre(self):
        (x0, x1), (y0, y1) = config.AREA
        points = [(x0, y0), (x1, y0), (x0, y1), (x1, y1),
                  ((x0 + x1) / 2, (y0 + y1) / 2)]
        for x, y in points:
            angles = kinematics.solve(x, y)
            self.assertIsNotNone(angles, "corner should be reachable")
            px, py = pen_position(angles[0], angles[1])
            self.assertAlmostEqual(px, x, delta=0.5)
            self.assertAlmostEqual(py, y, delta=0.5)

    def test_more_points(self):
        for x, y in [(50, 60), (150, 200), (100, 30), (180, 140)]:
            alpha, beta = kinematics.solve(x, y)
            px, py = pen_position(alpha, beta)
            self.assertAlmostEqual(px, x, delta=0.5)
            self.assertAlmostEqual(py, y, delta=0.5)

    def test_out_of_reach(self):
        self.assertIsNone(kinematics.solve(400, 400))

    def test_at_the_shoulder(self):
        # d = 0 would divide by zero, so solve() must return None
        self.assertIsNone(kinematics.solve(-50, 139.5))


class TestGetTargetAngles(unittest.TestCase):

    def make_state(self, mode):
        return {"mode": mode, "x": 0.0, "y": 0.0,
                "alpha": 75.0, "beta": 35.0}

    def test_joint_mode(self):
        state = self.make_state(config.MODE_JOINT)
        alpha, beta = kinematics.get_target_angles(state, 0, 65535)
        self.assertAlmostEqual(alpha, config.SHOULDER_LIMITS[0])
        self.assertAlmostEqual(beta, config.ELBOW_LIMITS[1])

    def test_drawing_mode_sets_x_and_y(self):
        state = self.make_state(config.MODE_XY)
        alpha, beta = kinematics.get_target_angles(state, 0, 0)
        self.assertAlmostEqual(state["x"], config.AREA[0][0])
        self.assertAlmostEqual(state["y"], config.AREA[1][0])
        self.assertEqual((alpha, beta), kinematics.solve(state["x"], state["y"]))


if __name__ == "__main__":
    unittest.main()
