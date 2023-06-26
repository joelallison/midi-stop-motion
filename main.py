import pretty_midi
import cv2 as cv

'''

I think short videos is best

The videos need to be cut to length so that anticipation time is taken into account and stuff

process: 
    - (into an array) convert midi events into timestamps via tempo information
    - process that array into the states system
    - state object: label & timestamp
    - lookup image via label (dictionary)
    - stitch together the image

'''
class drum_hit:
    def __init__(self, drum, hit_type):
        self.drum = drum
        self.hit_type = hit_type

class drum_state:
    def __init__(self, left_hand, right_hand, kick, hi_hat):
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.kick = kick
        self.hi_hat_open = hi_hat

    def __init__(self, left_hand, right_hand):
        self.left_hand = left_hand
        self.right_hand = right_hand

    def to_string(self):
        return "Left hand: " + self.left_hand + "\tRight hand: " + self.right_hand

#this is for the Logic Pro X Drum Kit Designer mapping
drum_mapping = {
    28 : drum_hit("crash_left", "stop"),
    29 : drum_hit("crash_right", "stop"),
    31 : drum_hit("hi_hat", "foot_splash"),
    32 : drum_hit("snare", "rimshot_edge"),
    33 : drum_hit("hi_hat", "foot_close"),
    34 : drum_hit("snare", "edge"),
    35 : drum_hit("kick", "-"),
    36 : drum_hit("kick", "-"),
    37 : drum_hit("snare", "sidestick"),
    38 : drum_hit("snare", "center"),
    39 : drum_hit("clap", "-"),
    40 : drum_hit("snare", "rimshot"),
    41 : drum_hit("low_tom", "1"),
    42 : drum_hit("hi_hat", "closed"),
    43 : drum_hit("low_tom", "2"),
    44 : drum_hit("hi_hat", "foot_close"),
    45 : drum_hit("mid_tom", "1"),
    46 : drum_hit("hi_hat", "open"),
    47 : drum_hit("mid_tom", "2"),
    48 : drum_hit("hi_tom", "1"),
    49 : drum_hit("crash_left", "-"),
    50 : drum_hit("hi_tom", "2"),
    51 : drum_hit("ride", "out"),
    52 : drum_hit("ride", "edge"),
    53 : drum_hit("ride", "bell"),
    54 : drum_hit("tambourine", "-"),
    56 : drum_hit("cowbell", "-"),
    57 : drum_hit("crash_right", "-"),
    59 : drum_hit("ride", "in")
}

whitelist = ["kick", "snare", "hi_hat", "ride"]

def create_all_possible_states():
    states = []
    drums = []

    for item in drum_mapping:
        if (drum_mapping.get(item).drum in whitelist):
            if not (drum_mapping.get(item).drum == "kick" or drum_mapping.get(item).hit_type[:4] == "foot"):
                if drum_mapping.get(item).drum not in drums:
                    if drum_mapping.get(item).drum == "hi_hat":
                        drums.append(drum_mapping.get(item).drum + "." + drum_mapping.get(item).hit_type)
                    else:
                        drums.append(drum_mapping.get(item).drum)

    for drum1 in drums:
        for drum2 in drums:
            if not (drum1 == drum2):
                states.append(drum_state(drum1, drum2))
        states.append(drum_state("-", drum1))
        states.append(drum_state(drum1, "-"))

    return states


count = 0
for state in create_all_possible_states():
    print(str(count) + "\t" + state.to_string())
    count += 1

'''
midi_data = pretty_midi.PrettyMIDI('test.mid')
print("duration:",midi_data.get_end_time())
print(f'{"drum":>10} {"type":>10}{"start":>10} {"end":>10}')
for instrument in midi_data.instruments:
    for note in instrument.notes:
        print(f'{drum_mapping[note.pitch].drum:10} {drum_mapping[note.pitch].hit_type:10} {note.start:10} {note.end:10}')
'''