#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def clean_line(line):
    content, *_ = line.split('#', 1) # remove comments
    try:
        return int(content.strip(), 2) # convert to int
    except:
        return None

code_addr = sys.argv[1]
parsed_lines = [clean_line(line) for line in open(code_addr, 'r')]
instructions = [instruct for instruct in parsed_lines if instruct is not None]


cpu = CPU()

cpu.load(instructions)
cpu.run()