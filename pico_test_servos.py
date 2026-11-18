# pico_test_servos.py  (tests T3 and T5, runs on the PICO with the jig)
# Owner: Abdulelah Aburehla
#
# Upload this file to the Pico next to the project files, open it in Thonny
# and press Run. Keep a hand near the USB cable and unplug it if the arm
# buzzes or touches the jig.
#
# T3: each arm servo steps from its min limit to its max limit in 5 degree
#     steps (through servo_driver only), then we ask for 10 degrees past
#     each limit. Pass: no buzzing, no contact with the jig, and the
#     out-of-range requests stop at the limit.
# T5: the pen goes down and up 10 times. Pass: no missed toggles.

import time
import config
import servo_driver

servos = servo_driver.init_servos()
servo_driver.set_pen(servos, False)

# start in the middle of both ranges
mid_alpha = (config.SHOULDER_LIMITS[0] + config.SHOULDER_LIMITS[1]) / 2
mid_beta = (config.ELBOW_LIMITS[0] + config.ELBOW_LIMITS[1]) / 2
servo_driver.move_arm(servos, mid_alpha, mid_beta)
time.sleep_ms(1000)


def sweep(joint, low, high):
    """Steps one joint from low to high in 5 degree steps, other joint in the middle."""
    angle = low
    while angle <= high:
        if joint == "shoulder":
            servo_driver.move_arm(servos, angle, mid_beta)
        else:
            servo_driver.move_arm(servos, mid_alpha, angle)
        print(joint, angle)
        time.sleep_ms(300)
        angle = angle + 5


try:
    print("T3: shoulder sweep")
    sweep("shoulder", config.SHOULDER_LIMITS[0], config.SHOULDER_LIMITS[1])
    print("T3: shoulder 10 degrees past each limit (should stop at the limit)")
    sweep("shoulder", config.SHOULDER_LIMITS[1] + 10, config.SHOULDER_LIMITS[1] + 10)
    sweep("shoulder", config.SHOULDER_LIMITS[0] - 10, config.SHOULDER_LIMITS[0] - 10)

    print("T3: elbow sweep")
    sweep("elbow", config.ELBOW_LIMITS[0], config.ELBOW_LIMITS[1])
    print("T3: elbow 10 degrees past each limit (should stop at the limit)")
    sweep("elbow", config.ELBOW_LIMITS[1] + 10, config.ELBOW_LIMITS[1] + 10)
    sweep("elbow", config.ELBOW_LIMITS[0] - 10, config.ELBOW_LIMITS[0] - 10)

    servo_driver.move_arm(servos, mid_alpha, mid_beta)
    print("T5: pen down/up 10 times")
    for i in range(10):
        servo_driver.set_pen(servos, True)
        time.sleep_ms(500)
        servo_driver.set_pen(servos, False)
        time.sleep_ms(500)
        print("toggle", i + 1)
    print("Done. Write down what you saw in the T3/T5 GitHub issues.")
finally:
    servo_driver.set_pen(servos, False)
    time.sleep_ms(300)
    servo_driver.stop_servos(servos)
