import tkinter as tk
from time import time
import json
import os

model_sentence = 'My name is {user} and I am authenticating myself'
users_data = {}

def key(event, user, sentence_label):
    users_data.setdefault(user, {'keys_pressed': 0, 'start_time': time()})
    users_data[user]['keys_pressed'] += 1

def quit(event, user):
    elapsed_time = time() - users_data[user]['start_time']
    total_words = users_data[user]['keys_pressed'] // 4.79
    wpm = total_words / (elapsed_time / 60) if elapsed_time != 0 else 0

    save_data(user, wpm)
    authenticate_user(user, wpm)
    master.destroy()

def save_data(user, wpm):
    users_data_folder = "User Data"
    os.makedirs(users_data_folder, exist_ok=True)

    data_file = f"{users_data_folder}/{user}_wpm_data.json"
    data = []
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            data = json.load(file)

    data.append(wpm)
    with open(data_file, "w") as file:
        json.dump(data, file)

def authenticate_user(user, new_wpm):
    data_file = f"User Data/{user}_wpm_data.json"
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            data = json.load(file)
            if len(data) > 1:
                avg_wpm = sum(data[:-1]) / (len(data) - 1)
                if abs(new_wpm - avg_wpm) <= 5.5:
                    show_message(f"User {user} authenticated.")
                else:
                    show_message(f"User {user} not authenticated. Too much variation in typing speeds.")
    else:
        show_message(f"No previous WPM results for user {user}. Please type the sentence three times to get results.")
        get_input(user, model_sentence.format(user=user), repeat=3)
        show_message(f"Initial data has been registered for user {user}. Please authenticate again.")

def show_message(message):
    message_window = tk.Tk()
    message_window.title("Update")
    
    message_label = tk.Label(message_window, text=message, pady=20)
    message_label.pack()
    
    understood_button = tk.Button(message_window, text="Understood", command=message_window.destroy)
    understood_button.pack(pady=5)
    
    message_window.mainloop()

def get_user_identity():
    instruction_window = tk.Tk()
    instruction_window.title("Authentication Instructions")
    
    instruction_label = tk.Label(instruction_window, text="This system is designed to authenticate you based on your typing behaviour.\n\n1. Enter a username and follow the instructions. New users are required to give an initial result in order to be authenticated.\n2. It is important to type naturally otherwise authentication will be affected.\n3. The model sentence IS NOT case sensitive. Your username IS case sensitive.", pady=5)
    instruction_label.pack()
    
    understood_button = tk.Button(instruction_window, text="Understood", command=instruction_window.destroy)
    understood_button.pack(pady=5)
    
    instruction_window.mainloop()
    
    username_window = tk.Tk()
    username_window.title("Username")
    
    username_label = tk.Label(username_window, text="Please enter username:", pady=5)
    username_label.pack()
    
    user_entry = tk.Entry(username_window)
    user_entry.pack()
    
    submit_button = tk.Button(username_window, text="Submit", command=lambda: process_username(user_entry.get(), username_window))
    submit_button.pack(pady=5)
    
    username_window.mainloop()

def process_username(user, window):
    window.destroy()
    
    data_file = f"User Data/{user}_wpm_data.json"
    if os.path.exists(data_file):
        sentence = model_sentence.format(user=user)
        get_input(user, sentence)
    else:
        authenticate_user(user, 0)

def get_input(user, sentence, repeat=1):
    global master
    master = tk.Tk()
    
    sentence_label = tk.Label(master, text=f"User {user} please type: '{sentence}'", pady=5)
    sentence_label.pack()
    
    e = tk.Entry(master)
    e.pack()
    e.bind("<Key>", lambda event: key(event, user, sentence_label))
    
    if repeat > 1:
        e.bind("<Return>", lambda event: repeat_input(event, user, sentence, repeat-1))
    else:
        e.bind("<Return>", lambda event: quit(event, user))
    
    master.mainloop()

def repeat_input(event, user, sentence, repeat):
    global master
    master.destroy()
    get_input(user, sentence, repeat)

get_user_identity()