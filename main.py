import pretty_midi
import tkinter as tk
from tkinter import ttk

framerate = 12
inverse_framerate = 1/framerate
total_frames = 0

def load_file():
    global midi_data
    global total_frames

    midi_data = pretty_midi.PrettyMIDI(filename_entry.get())
    total_frames = int(framerate * midi_data.get_end_time())
    total_frames_value.config(text=total_frames)

    notes_per_frame = [[] for i in range(total_frames)]

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            for i in range(total_frames):
                if (i * inverse_framerate >= note.start) and (i * inverse_framerate < note.end):
                    print(note.pitch, "\t", i * inverse_framerate, " : ", note.start, " : ", note.end)
                    notes_per_frame[i].append(note.pitch)

    print(notes_per_frame)


root = tk.Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
filename_label = tk.Label(frm, text="File name: ")
filename_label.grid(column=0, row=0)

filename_entry = tk.Entry(frm, text="")
filename_entry.grid(column=1, row=0)

tk.Button(frm, text="Load", command=load_file).grid(column=2, row=0)

total_frames_label = tk.Label(frm, text="Total frames: ")
total_frames_label.grid(column=0, row=1)

total_frames_value = tk.Label(frm, text="")
total_frames_value.grid(column=1, row=1)

root.mainloop()