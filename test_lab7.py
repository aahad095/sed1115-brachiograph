# test_lab7.py
# SED 1115 - Lab 7: unit tests for the G-Code parser and the servo translator.
# Runs on the Pico (open it in Thonny and press Run) or on a laptop with normal Python.
# It does not move any servos.

from gcode_parser import parse_line
from servo_translator import translate

passed = 0
failed = 0


def check(name, result, expected):
    global passed, failed
    if result == expected:
        passed += 1
        print("PASS:", name)
    else:
        failed += 1
        print("FAIL:", name, "- got", result, "expected", expected)


def test_parse_line():
    check("G1 with S and E", parse_line("G1 S62.858 E54.284"), ("G1", {"S": 62.858, "E": 54.284}))
    check("G1 with only S", parse_line("G1 S90"), ("G1", {"S": 90.0}))
    check("G1 with only E", parse_line("G1 E45"), ("G1", {"E": 45.0}))
    check("G1 with no angles", parse_line("G1"), ("G1", {}))
    check("M3 pen down", parse_line("M3"), ("M3", {}))
    check("M5 pen up", parse_line("M5"), ("M5", {}))
    check("M18 disable", parse_line("M18"), ("M18", {}))
    check("newline and extra spaces", parse_line("  G1 S56.073 E30.52 \n"), ("G1", {"S": 56.073, "E": 30.52}))
    check("lowercase", parse_line("g1 s10 e20"), ("G1", {"S": 10.0, "E": 20.0}))
    check("blank line", parse_line(""), (None, {}))
    check("only a newline", parse_line("\n"), (None, {}))
    check("comment line", parse_line("; this is a comment"), (None, {}))
    check("comment after a command", parse_line("M3 ; pen down"), ("M3", {}))
    check("bad number is skipped", parse_line("G1 Sabc E20"), ("G1", {"E": 20.0}))


def test_translate():
    check("translate 0 degrees", translate(0), 1638)
    check("translate 180 degrees", translate(180), 8192)
    check("translate 90 degrees", translate(90), 4915)
    check("translate below 0 is clamped", translate(-20), 1638)
    check("translate above 180 is clamped", translate(250), 8192)


def test_gcode_file(filename):
    """Checks that every line of a G-Code file is a known command with safe angles."""
    known = ["G1", "M3", "M5", "M18"]
    ok = True
    try:
        with open(filename, "r") as f:
            for line in f:
                command, params = parse_line(line)
                if command is None:
                    continue
                if command not in known:
                    ok = False
                for letter in params:
                    if letter not in ["S", "E"] or params[letter] < 0 or params[letter] > 180:
                        ok = False
    except OSError:
        print("SKIP:", filename, "is not uploaded")
        return
    check(filename + " only has known commands and angles 0-180", ok, True)


test_parse_line()
test_translate()
for name in ["line.gcode", "square.gcode", "circle.gcode", "circle_and_square.gcode"]:
    test_gcode_file(name)

print()
print(passed, "passed,", failed, "failed")
