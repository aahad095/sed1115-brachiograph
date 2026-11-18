#!/bin/bash
# Deliverable C: opens the new issues (#34-#43) for everything that is
# still missing or untested. Issues #1-#33 (one per function) were opened
# for Deliverable B and are closed by the pull request that adds the code.
# Needs the GitHub CLI (https://cli.github.com). Run once from the repo folder.
# Fill in the two missing GitHub usernames first.

AHAD="aahad095"
ABDULELAH="FILL_IN"
CLAIRE="FILL_IN"

gh label create test --color 0E8A16 --description "On-jig or unit test still to run" 2>/dev/null

gh issue create --label test --assignee "$ABDULELAH" --title "T3: measure servo limits and run the servo sweep" --body "Run pico_test_servos.py on the jig. Find the real min/max angle for the shoulder and elbow without touching the jig and put them in SHOULDER_LIMITS and ELBOW_LIMITS in config.py. Right now config.py uses the safe ranges from the Lab 7 G-code files (shoulder 45-110, elbow 10-60). Schedule task 3 / task 10."
gh issue create --label test --assignee "$AHAD" --title "Measure the jig and set the safe drawing area (AREA)" --body "Measure where the paper sits and which part of it the arm can reach inside the servo limits from #34. Update AREA in config.py (it is still the guess ((20,190),(20,250))). Schedule task 4."
gh issue create --label bug --assignee "$AHAD" --title "Drawing mode: calibrate servo offsets and direction" --body "kinematics.solve() gives joint angles that match the brief (139.4, 73 -> 120.3, 99.3; unit test passes), but SHOULDER_OFFSET and ELBOW_OFFSET are still 0, so the servo angles don't line up with the paper yet. Most targets get clamped to the servo limits. Use joint mode to find the servo angles for 3 known points, then work out the offsets (and check if a servo turns the opposite way, which would need servo_angle = offset - joint_angle). Blocks the first full drawing (task 15) and T6."
gh issue create --label test --assignee "$CLAIRE" --title "T1/T2: test the knobs and buttons on the Pico" --body "Run pico_test_inputs.py. T1 pass: each knob covers at least 95% of 0-65535 and moves less than 200 counts when still. T2 pass: 20 presses counted as 20, holding for 2 s counts as 1. The logic already passes the laptop tests with fake buttons."
gh issue create --label test --assignee "$CLAIRE" --title "T5: pen up/down on the jig" --body "Run the T5 part of pico_test_servos.py, then toggle the pen 10 times with main.py while the arm moves. Check PEN_UP = 0 and PEN_DOWN = 30 (from Lab 7) actually lift and touch the paper on our jig."
gh issue create --label question --assignee "$CLAIRE" --title "Confirm the button pin numbers (GP10 / GP11)" --body "config.py uses GP10 for the pen button and GP11 for the mode button. Check against the lab accessory board and fix config.py if they are different."
gh issue create --label test --assignee "$AHAD" --title "T6: position accuracy (5 targets and a 50 mm square)" --body "After #36. Drive the pen to the 5 crosses on the target sheet and draw a 50 mm square. Pass: every target within 5 mm, square sides within +-3 mm. Whole team runs it."
gh issue create --label test --assignee "$AHAD" --title "T7: smoothness and loop timing; tune DEADBAND and MAX_STEP_DEG" --body "Add a ticks_us() measurement around run_once(), log 1000 loops. Pass: worst loop under 20 ms, no visible wobble with the knobs still, no slamming when a knob is spun fast. Tune DEADBAND (200) and MAX_STEP_DEG (2.0) in config.py. Schedule task 16 / 18."
gh issue create --label test --assignee "$ABDULELAH" --title "T8: endurance and restart" --body "Draw for 15 minutes while printing gc.mem_free(), then unplug and plug back in. Pass: no crash or MemoryError, free memory steady, main.py restarts with the pen up."
gh issue create --label bug --assignee "$AHAD" --title "Move the Lab 7 files out and merge Initial-Design into main" --body "main still has the Lab 7 G-code main.py, and the Initial-Design branch still carries gcode_parser.py, lab7_skeleton.py, test_lab7.py and the .gcode files. Move them into a lab7/ folder, then merge Initial-Design into main, because the demo runs from main."
