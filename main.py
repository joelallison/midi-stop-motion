import mido as mi
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

mid = mi.MidiFile('all_the_drums.mid')
for msg in mid.tracks[0]:
    if not msg.is_meta:
        print(msg)

class drum_hit:
    def __init__(self, drum, hit_type):
        self.drum = drum
        self.hit_type = hit_type

#this is for the Logic Pro X Drum Kit Designer mapping
drum_mapping = {
    28 : drum_hit("crash_left", "stop"),
    29 : drum_hit("crash_right", "stop"),
    31 : drum_hit("hi_hat", "foot_splash"),
    32 : drum_hit("snare", "rimshot_edge"),
    33 : drum_hit("hi_hat", "foot_close"),
    34 : drum_hit("snare", "edge"),
    35 : drum_hit("kick", None),
    36 : drum_hit("kick", None),
    37 : drum_hit("snare", "sidestick"),
    38 : drum_hit("snare", "center"),
    39 : drum_hit("clap", None),
    40 : drum_hit("snare", "rimshot"),
    41 : drum_hit("low_tom", "1"),
    42 : drum_hit("hi_hat", "closed"),
    43 : drum_hit("low_tom", "2"),
    44 : drum_hit("hi_hat", "foot_close"),
    45 : drum_hit("mid_tom", "1"),
    46 : drum_hit("hi_hat", "open"),
    47 : drum_hit("mid_tom", "2"),
    48 : drum_hit("hi_tom", "1"),
    49 : drum_hit("crash_left", None),
    50 : drum_hit("hi_tom", "2"),
    51 : drum_hit("ride", "out"),
    52 : drum_hit("ride", "edge"),
    53 : drum_hit("ride", "bell"),
    54 : drum_hit("tambourine", None),
    56 : drum_hit("cowbell", None),
    57 : drum_hit("crash_right", None),
    59 : drum_hit("ride", "in")
}

class Drum_state:
    def __init__(self, left_hand, right_hand, kick, hi_hat_open):
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.kick = kick
        self.hi_hat_open = hi_hat_open

state = Drum_state('snare', 'tom', False, False)

