import pretty_midi
import cv2 as cv

'''
plan:

figure out all the different combinations of drum hits. [I only have two hands]
    ---> number of things to hit + (number of things to hit-1 * (number of things to hit))...?
    
figure out a way to label the states...?
could just be like snare_tom1, in the form lefthand_righthand
and a single hit would be something like snare_0 or 0_tom1

should it be single images or short videos? both options? try with single images first?

whether hi hat is open should be taken into account!!
therefore might need double the amount of photos/videos?

and the pedal hi hat whole thing should be taken into account and be allowed to be processed separately kinda

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

def create_all_possible_states():
    states = []
    stick_hits = {}

    for item in drum_mapping:
        if not (drum_mapping.get(item).drum == "kick" or drum_mapping.get(item).hit_type[:4] == "foot"):
            stick_hits.update({item : drum_mapping.get(item)})

    for item in stick_hits:
        second_hand_hits = {}

        for hit in stick_hits:
            if not (stick_hits.get(hit).drum == stick_hits.get(item).drum):
                second_hand_hits.update({hit: stick_hits.get(hit)})

        for secondary_item in second_hand_hits:
            states.append(drum_state(stick_hits.get(item), stick_hits.get(secondary_item), False, False))
            states.append(drum_state(stick_hits.get(item), stick_hits.get(secondary_item), False, True))
            states.append(drum_state(stick_hits.get(item), stick_hits.get(secondary_item), True, False))
            states.append(drum_state(stick_hits.get(item), stick_hits.get(secondary_item), True, True))

    return states

count = 0
for x in create_all_possible_states():
    print(count, "\t", x.right_hand.drum + "." + x.right_hand.hit_type, " ", x.left_hand.drum + "." + x.left_hand.hit_type, " ", x.kick, " ", x.hi_hat_open)
    count += 1

'''
midi_data = pretty_midi.PrettyMIDI('test.mid')
print("duration:",midi_data.get_end_time())
print(f'{"drum":>10} {"type":>10}{"start":>10} {"end":>10}')
for instrument in midi_data.instruments:
    for note in instrument.notes:
        print(f'{drum_mapping[note.pitch].drum:10} {drum_mapping[note.pitch].hit_type:10} {note.start:10} {note.end:10}')
'''