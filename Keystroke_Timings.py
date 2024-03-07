import tkinter
from time import time

sample = "once upon a time"
sample_length = len(sample)
stroke_times = list(range(sample_length))  # Initialize stroke_times as a list
delta_times = stroke_times[:]  # Initialize delta_times as a copy of stroke_times
boolType = True
i = 0

def key(event):
    global i
    global boolType
    if event.char == '\r':
        e.unbind("<Key>")
        return
    end_time = time()
    if str(event.char) != sample[i]:
        boolType = False
        print("poor loser! PRESS Enter")
    stroke_times[i] = end_time - start_time  # date of stroke
    i += 1

def quit(event):
    global i
    global stroke_times, delta_times
    e.destroy()
    master.destroy()
    delta_times = [x - y for x, y in zip(stroke_times[1:], stroke_times[:-1])]
    i = 0
    stroke_times = list(range(sample_length))  # Reinitialize stroke_times
    if len(delta_times) != sample_length - 1:
        print("you FAILED!! go back to school")
    else:
        with open("keystroke_data.pickle", "a") as file:
            file.write(" ".join(str(x) for x in delta_times) + "\n")
        print("Results written to keystroke_data.pickle")

start_time = end_time = 0

def get_input():
    global e, master
    global boolType
    master = tkinter.Tk()
    e = tkinter.Entry(master)
    e.pack()
    e.focus_set()
    e.bind("<Key>", key)
    e.bind("<Return>", quit)
    print("___________________________________________")
    print("TYPE : 'once upon a time'")
    global start_time
    start_time = time()
    tkinter.mainloop()

    if delta_times.count(1) != 0 or boolType is False:
        boolType = True
        return get_input()
    else:
        return delta_times

# Run the function to capture keystrokes and write to the file
get_input()
