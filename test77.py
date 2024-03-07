import tkinter
from time import time

sample = "This is a test of your typing skills"
sample_length = len(sample)
stroke_times = [0] * sample_length  # Initialize stroke_times as a list
delta_times = stroke_times[:]  # Initialize delta_times as a copy of stroke_times
boolType = True
i = 0
incorrect_message_displayed = False

def key(event):
    global i
    global boolType
    global incorrect_message_displayed
    end_time = time()
    if i < sample_length:
        if str(event.char) != sample[i]:
            if not incorrect_message_displayed:
                boolType = False
                print("Incorrect character typed. Keep typing...")
                incorrect_message_displayed = True
        else:
            incorrect_message_displayed = False  # Reset flag if correct character typed
        stroke_times[i] = end_time - start_time  # date of stroke
        i += 1

def quit(event):
    global i
    global stroke_times, delta_times
    e.unbind("<Key>")
    e.destroy()
    master.destroy()
    delta_times = [x - y for x, y in zip(stroke_times[1:], stroke_times[:-1])]
    if len(delta_times) != sample_length - 1:
        print("you FAILED!! go back to school")
    else:
        with open("keystroke_data.pickle", "a") as file:
            file.write(" ".join(str(x) for x in delta_times) + "\n")
        print("Results written to keystroke_data.pickle")
    return "break"  # Prevents default behavior of <Return> key

start_time = end_time = 0

def get_input():
    global e, master
    global boolType, i
    master = tkinter.Tk()
    e = tkinter.Entry(master)
    e.pack()
    e.focus_set()
    e.bind("<Key>", key)
    e.bind("<Return>", quit)
    print("___________________________________________")
    print("TYPE : 'This is a test of your typing skills'")
    global start_time
    start_time = time()
    tkinter.mainloop()

# Run the function to capture keystrokes and write to the file
get_input()
