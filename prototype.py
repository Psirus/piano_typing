import mido
from subprocess import Popen, PIPE

key_a = '''key a '''

def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence.encode())

mpk = mido.get_input_names()[0]
with mido.open_input(mpk) as inport:
    for msg in inport:
        if msg.type == "note_on":
            keypress(key_a)
