# main.py
# Owner: Abdulelah Aburehla (reviewed by all three of us)
# Designed by: Abdulelah Aburehla
# Tested by:   Abdulelah Aburehla (tests/test_main_logic.py), whole team on the jig
#
# The entry point. Runs automatically when the Pico powers up.
# This file is only a list of calls to the functions in the other files,
# so it shows the calling structure of the whole program.
#
# Files to upload to the Pico: main.py, config.py, input_handler.py,
# plotter_state.py, kinematics.py, servo_driver.py, servo_translator.py

import time

import config
import input_handler
import plotter_state
import kinematics
import servo_driver


def setup():
    """
    Owner:   Abdulelah Aburehla
    Purpose: Get everything ready before the loop starts.
    Inputs:  none
    Returns: tuple (inputs, servos, state) - the three dicts the loop uses
    How:     Call the three "create" functions, then lift the pen so the
             program always starts with the pen up.
    Changes: creates inputs, servos and state (through the functions it calls)
    """
    inputs = input_handler.init_inputs()
    servos = servo_driver.init_servos()
    state = plotter_state.make_state()
    servo_driver.set_pen(servos, False)
    return (inputs, servos, state)


def run_once(inputs, servos, state, now_ms):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Do one full pass: read the user, do the maths, move the arm.
    Inputs:  inputs - dict from init_inputs()
             servos - dict from init_servos()
             state  - the live state dict
             now_ms - int, current time from time.ticks_ms()
    Returns: nothing
    How:     Read inputs -> update pen and mode -> get the target angles ->
             limit how far each joint moves -> move the servos.
    Changes: state["alpha"], state["beta"] (other keys through the helpers)
    """
    x_count, y_count, pen_pressed, mode_pressed = input_handler.read_inputs(
        inputs, state, now_ms)

    plotter_state.update_pen(state, pen_pressed)
    plotter_state.update_mode(state, mode_pressed)

    alpha, beta = kinematics.get_target_angles(state, x_count, y_count)
    state["alpha"] = kinematics.limit_step(
        state["alpha"], alpha, config.MAX_STEP_DEG)
    state["beta"] = kinematics.limit_step(
        state["beta"], beta, config.MAX_STEP_DEG)

    servo_driver.move_arm(servos, state["alpha"], state["beta"])
    servo_driver.set_pen(servos, state["pen_down"])


def wait_for_next_loop(start_ms):
    """
    Owner:   Abdulelah Aburehla
    Purpose: Make every loop take 20 ms, however long the work took.
    Inputs:  start_ms - int, time.ticks_ms() from the start of this loop
    Returns: nothing
    How:     Work out how long the loop has taken so far and sleep for
             whatever is left of config.LOOP_MS. If we are already late,
             don't sleep at all.
    Changes: nothing
    """
    used_ms = time.ticks_diff(time.ticks_ms(), start_ms)
    if used_ms < config.LOOP_MS:
        time.sleep_ms(config.LOOP_MS - used_ms)


def main():
    """
    Owner:   Abdulelah Aburehla
    Purpose: Entry point of the program.
    Inputs:  none
    Returns: never returns (loops until the Pico is unplugged)
    How:     Call setup() once, then repeat forever: note the time, do one
             pass, do the housekeeping, wait for the rest of the 20 ms.
             If the program is stopped (Stop in Thonny, or an error), the
             "finally" part lifts the pen and lets the servos go limp, so
             the pen never stays down on the paper.
    Changes: nothing directly
    """
    inputs, servos, state = setup()
    print("BrachioGraph ready. Mode button switches draw/joint mode.")
    try:
        while True:
            start_ms = time.ticks_ms()
            run_once(inputs, servos, state, start_ms)
            plotter_state.do_housekeeping(state)
            wait_for_next_loop(start_ms)
    finally:
        servo_driver.set_pen(servos, False)
        time.sleep_ms(300)
        servo_driver.stop_servos(servos)
        print("Stopped. Pen up, servos off.")


if __name__ == "__main__":
    main()
