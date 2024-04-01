from time import time

sample = "This is a test of your typing skills"
sample_length = len(sample)

def read_keypress_times_from_file(file_name):
    keypress_times = []
    with open(file_name, "r") as file:
        for line in file:
            keypress_times.append(list(map(float, line.split())))
    return keypress_times

def calculate_typing_speed(keypress_times):
    typing_speeds = []
    for times in keypress_times:
        if len(times) == sample_length:
            delta_times = [times[i] - times[i-1] for i in range(1, len(times))]
            average_speed = sum(delta_times) / len(delta_times) if delta_times else 0
            typing_speed = 60 / average_speed if average_speed != 0 else 0
            typing_speeds.append(typing_speed)
        else:
            typing_speeds.append(None)
    return typing_speeds

def determine_typist_typing_speed(file_name):
    keypress_times = read_keypress_times_from_file(file_name)
    typing_speeds = calculate_typing_speed(keypress_times)
    
    threshold = 30  # Adjust threshold as needed
    
    for idx, speed in enumerate(typing_speeds, 1):
        if speed is not None:
            if speed >= threshold:
                print("Typist {} is typing at {:.2f} characters per minute.".format(idx, speed))
            else:
                print("Typist {} is not typing at an acceptable speed.".format(idx))
        else:
            print("Typist {} has insufficient data for typing speed calculation.".format(idx))

# Specify the file containing keypress times
file_name = "keystroke_data.pickle"

# Determine typing speed of typists based on keypress times
determine_typist_typing_speed(file_name)