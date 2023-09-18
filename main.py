import pretty_midi
import tkinter as tk
from tkinter import ttk

framerate = 12
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


    global video_load_labels
    video_load_labels = []

    global video_load_entries
    video_load_entries = []

    global video_load_hold_checkbuttons
    video_load_hold_checkbuttons = []

    global video_load_ignore_checkbuttons
    video_load_ignore_checkbuttons = []


    global combination_to_filename
    combination_to_filename = {}

    for i in range(len(unique_combinations)):
        combination_to_filename[unique_combinations[i]] = ""

        video_load_labels.append(tk.Label(frm, text=str(unique_combinations[i]) + ": "))
        video_load_labels[i].grid(column=0, row=row + i)

        video_load_entries.append(tk.Entry(frm, text=""))
        video_load_entries[i].grid(column=1, columnspan=2, row=row + i)

        tk.Label(frm, text="Hold: ").grid(column=3, row=row + i)
        video_load_hold_checkbuttons.append(tk.Checkbutton(frm))
        video_load_hold_checkbuttons[i].grid(column=4, row=row + i)

        tk.Label(frm, text="Ignore: ").grid(column=5, row=row + i)
        video_load_ignore_checkbuttons.append(tk.Checkbutton(frm))
        video_load_ignore_checkbuttons[i].grid(column=6, row=row + i)

    tk.Button(frm, text="Load videos", command=load_videos).grid(column=0, columnspan=3, row=row+i+1)


def load_videos():
    for i in range(len(video_load_entries)):
        print(get_filename_for_index(i))
def get_filename_for_index(index):
    return video_load_entries[index].get()


root = tk.Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
filename_label = tk.Label(frm, text="File name: ")
filename_label.grid(column=0, row=0)

filename_entry = tk.Entry(frm, text="")
filename_entry.grid(column=1, row=0)

tk.Button(frm, text="Load", command=load_file).grid(column=2, row=0)

'''
total_frames_label = tk.Label(frm, text="Total frames: ")
total_frames_label.grid(column=0, row=1)

total_frames_value = tk.Label(frm, text="")
total_frames_value.grid(column=1, row=1)
'''

root.mainloop()