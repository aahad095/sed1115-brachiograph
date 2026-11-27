# gcode_parser.py
# SED 1115 - Lab 7: Plotter Control
# G-Code parser: turns one line of G-Code into a command and its parameters.
# This file does not use any Pico hardware, so it can also be tested on a laptop.


def parse_line(line):
    """
    Splits one line of G-Code into a command and a dictionary of parameters.

    Examples:
        "G1 S62.858 E54.284"  ->  ("G1", {"S": 62.858, "E": 54.284})
        "M3"                  ->  ("M3", {})
        ""  (blank line)      ->  (None, {})

    The command is a string. The parameters go in a dictionary so we can
    look them up by their letter later on, like params["S"].
    """
    # anything after a ; is a comment, so we cut it off
    line = line.split(";")[0]

    # remove spaces and the newline at the start and end
    line = line.strip()

    # nothing left means a blank line (or a comment-only line)
    if line == "":
        return None, {}

    parts = line.split()
    command = parts[0].upper()

    params = {}
    for part in parts[1:]:
        letter = part[0].upper()
        try:
            value = float(part[1:])
        except ValueError:
            print("Bad parameter, skipped:", part)
            continue
        params[letter] = value

    return command, params
