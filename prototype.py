import mido
from subprocess import Popen, PIPE
import string

# MIDI
# c2 -> 48
# g2 -> 55
# 
# c4 -> 72
# g4 -> 79

# Left hand. Top keyboard (starting with space), bottom piano (around g2)
#   e a i u   w  c  l  v  x
# b a g f e   as gs fs ds d
# 59 -> 50
# (not correct anymore, but to get an idea)
left_hand = zip(range(59, 50, -1), ["space", "w", "e", "c", "a", "l", "i", "u", "x"])

# Right hand. Top keyboard (starting with space), bottom piano (around g4)
#   n r t d   k  h  g  f  q
# f g a b c   fs gs as cs d
# 77 -> 86
# (again, not correct anymore, but to get an idea)
right_hand = zip(range(77, 87), ["space", "k", "n", "h", "r", "g", "t", "d", "q", "y"])

# This is probably very personal. I have no idea how to go about this sensibly.
# What you see below is my adaptation of what keys I use most often in vim and
# how they fall on neo (keyboard layout).
KEYMAP = dict(list(left_hand) + list(right_hand))
KEYMAP[76] = "BackSpace"

def missing_letters():
    for char in string.ascii_lowercase:
        if char not in KEYMAP.values():
            print(char)
if False: missing_letters()

def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence.encode())

mpk = mido.get_input_names()[0]

if False:
    inport = mido.open_input(mpk)
    m = inport.receive()
    from IPython import embed; embed()

SHIFT = False

with mido.open_input(mpk) as inport:
    for msg in inport:
        if msg.type == "control_change" and msg.control == 67 and msg.value == 127:
            SHIFT = True
        if msg.type == "control_change" and msg.control == 67 and msg.value == 0:
            SHIFT = False
        if msg.type == "note_on" and msg.note in KEYMAP.keys():
            if SHIFT: keypress("keydown Shift_L ")
            keypress(f"key {KEYMAP[msg.note]} ")
            if SHIFT: keypress("keyup Shift_L ")
        if msg.type == "control_change" and msg.control == 64:
            keypress("key Escape ")

