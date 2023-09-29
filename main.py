import pretty_midi
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from functools import partial
import cv2
import moviepy as mv

# need anticipation variable --> global, 1 value for all videos
# preview anticipation feature? where you scroll the slider and it displays the frame that would hit on beat
#

framerate = 24
inverse_framerate = 1/framerate
total_frames = 0

def load_file():
    global midi_data
    global total_frames
    global notes_per_frame
    global unique_combinations

    midi_data = pretty_midi.PrettyMIDI(filename_entry.get())
    total_frames = int(framerate * midi_data.get_end_time())
    #total_frames_value.config(text=total_frames)

    notes_per_frame = [[] for i in range(total_frames)]

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            for i in range(total_frames):
                if (i * inverse_framerate >= note.start) and (i * inverse_framerate < note.end):
                    print(note.pitch, "\t", i * inverse_framerate, " : ", note.start, " : ", note.end)
                    notes_per_frame[i].append(note.pitch)

    unique_combinations = calculate_unique_combinations()

    create_mapping_list()


def calculate_unique_combinations():
    #note - an empty section is counted as a possible combination

    unique_combinations = []

    for i in range(len(notes_per_frame)):
        if (tuple(notes_per_frame[i]) not in unique_combinations):
            unique_combinations.append(tuple(notes_per_frame[i]))

    return unique_combinations

def create_mapping_list():
    global frm

    row, column = frm.grid_size()
    row = row-1 #cause of the load file line...

    #arrays of values for each note combination
    global video_load_buttons
    video_load_buttons = []

    global video_load_entries
    video_load_entries = []

    global video_load_hold_checkbuttons
    video_load_hold_checkbuttons = []

    global video_load_ignore_checkbuttons
    video_load_ignore_checkbuttons = []

    #mapping a video file to a note combination
    global combination_to_filename
    combination_to_filename = {}

    for i in range(len(unique_combinations)):
        combination_to_filename[unique_combinations[i]] = ""

        select_video_of_index = partial(select_video, i)
        tk.Button(frm, text=str(unique_combinations[i]) + ": ", command= select_video_of_index).grid(column=3, row=row + i)

        video_load_entries.append(tk.Entry(frm, text=""))
        video_load_entries[i].grid(column=4, columnspan=2, row=row + i)

        tk.Label(frm, text="Hold: ").grid(column=6, row=row + i)
        video_load_hold_checkbuttons.append(tk.Checkbutton(frm))
        video_load_hold_checkbuttons[i].grid(column=7, row=row + i)

        tk.Label(frm, text="Ignore: ").grid(column=8, row=row + i)
        video_load_ignore_checkbuttons.append(tk.Checkbutton(frm))
        video_load_ignore_checkbuttons[i].grid(column=9, row=row + i)

    tk.Button(frm, text="Load videos", command=load_videos).grid(column=3, columnspan=3, row=row+i+1)

    pack_still_selection()

def select_video(combination_id):
    print(combination_id)

def pack_still_selection():
    global frm
    global still_selection_frame
    global selected_frame_slider
    global img

    still_selection_frame = ttk.Frame(frm, padding=10)

    #16:9
    image_frame = tk.Frame(still_selection_frame, width=854, height=480)
    image_frame.pack()
    image_frame.place(anchor='center', relx=0.5, rely=0.5)

    img = ImageTk.PhotoImage(Image.open("no-image.jpeg"))
    tk.Label(still_selection_frame, image=img).grid(column=0, row=0)

    selected_frame_slider = tk.Scale(still_selection_frame, from_=0, to=1, orient=tk.HORIZONTAL)
    selected_frame_slider.grid(column=0, row=1, sticky="new")

    still_selection_frame.grid(column=0, columnspan=3, row=1, rowspan=20)

def load_videos():
    for i in range(len(video_load_entries)):
        print(get_filename_for_index(i))
def get_filename_for_index(index):
    return video_load_entries[index].get()

root = tk.Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

tk.Label(frm, text="File name: ").grid(column=0, row=0, sticky="ne")

filename_entry = tk.Entry(frm, text="")
filename_entry.grid(column=1, row=0, sticky="new")

tk.Button(frm, text="Load", command=load_file).grid(column=2, row=0, sticky="nw")

root.mainloop()