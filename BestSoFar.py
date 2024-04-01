import tkinter
from time import time

sample = "This is a test of your typing skills"
sample_length = len(sample)
users_data = {}  # Dictionary to store keypress timings for each user
threshold = 30  # Typing speed threshold
user_wpm = {}  # Dictionary to store WPM for each user
authenticated_users = {}  # Dictionary to store authenticated users and their last WPM

def key(event, user):
    global users_data
    if user not in users_data:
        users_data[user] = {'i': 0, 'stroke_times': [0] * sample_length, 'incorrect_message_displayed': False, 'start_time': time()}

    end_time = time()
    i = users_data[user]['i']
    stroke_times = users_data[user]['stroke_times']
    incorrect_message_displayed = users_data[user]['incorrect_message_displayed']
    start_time = users_data[user]['start_time']

    if i < sample_length:
        if event.char != sample[i]:
            if not incorrect_message_displayed:
                print("User {} - Incorrect character typed. Keep typing...".format(user))
                users_data[user]['incorrect_message_displayed'] = True
        else:
            users_data[user]['incorrect_message_displayed'] = False  # Reset flag if correct character typed
        stroke_times[i] = end_time - start_time  # Keypress time
        users_data[user]['i'] += 1

def quit(event, user):
    global users_data, user_wpm, authenticated_users
    i = users_data[user]['i']
    stroke_times = users_data[user]['stroke_times']
    start_time = users_data[user]['start_time']

    if i != sample_length:
        print("User {} - Incomplete typing. Please try again.".format(user))
    else:
        delta_times = [x - y for x, y in zip(stroke_times[1:], stroke_times[:-1])]
        if len(delta_times) != sample_length - 1:
            print("User {} - Incomplete typing. Please try again.".format(user))
        else:
            with open("keystroke_data_{}.txt".format(user), "a") as file:
                file.write("Keystroke times: " + " ".join(str(x) for x in delta_times) + "\n")
                
                # Calculate WPM
                total_time = sum(delta_times)
                wpm = (len(sample.split()) / (total_time / 60)) if total_time != 0 else 0
                user_wpm[user] = wpm
                file.write("WPM: {:.2f}\n".format(wpm))  # Write WPM to file
                
                # Authenticate user based on typing speed using initial WPM result for the first test
                if user in authenticated_users:
                    last_wpm = authenticated_users[user]
                    if abs(wpm - last_wpm) <= 3:
                        print("User {} authenticated for the second test.".format(user))
                    else:
                        print("User {} not authenticated for the second test. Typing speed significantly different.".format(user))
                else:
                    authenticated_users[user] = wpm  # Update authenticated user with initial WPM result
                    print("User {} authenticated for the first test.".format(user))
    
    master.destroy()  # Close the GUI

    # Authenticate user based on the last recorded WPM within +- 3
    if user in authenticated_users:
        last_wpm = authenticated_users[user]
        if abs(wpm - last_wpm) <= 3:
            print("User {} authenticated based on last recorded WPM.".format(user))
        else:
            print("User {} not authenticated based on last recorded WPM. Typing speed significantly different.".format(user))
    else:
            authenticated_users[user] = wpm  # Update authenticated user with new WPM

    # Prompt user to start a new GUI session for the second test
    get_user_identity()

def get_user_identity():
    global user
    user = input("Enter your username: ")
    get_input(user)

def get_input(user):
    global e, master
    master = tkinter.Tk()
    e = tkinter.Entry(master)
    e.pack()
    e.focus_set()
    e.bind("<Key>", lambda event: key(event, user))
    e.bind("<Return>", lambda event: quit(event, user))
    print("___________________________________________")
    print("User {} - TYPE: 'This is a test of your typing skills'".format(user))
    master.mainloop()

# Initial typing test for WPM calculation
get_user_identity()