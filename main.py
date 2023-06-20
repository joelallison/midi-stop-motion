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

process: 
    - (into an array) convert midi events into timestamps via tempo information
    - process that array into the states system
    - state object: label & timestamp
    - lookup image via label (dictionary)
    - stitch together the image

'''