import tkinter as tk
from time import time
import json
import os

sentence_template = 'My name is {user} and I am authenticating myself'
sample_length = len([char for char in sentence_template if char.isalpha() or char.isdigit()])
users_data = {}  # Dictionary to store keypress timings for each user

def key(event, user):
    if user not in users_data:
        users_data[user] = {'keys_pressed': 0, 'start_time': time()}

    users_data[user]['keys_pressed'] += 1

def quit(event, user):
    if user in users_data:
        elapsed_time = time() - users_data[user]['start_time']
        total_words = users_data[user]['keys_pressed'] // 5
        wpm = total_words / (elapsed_time / 60) if elapsed_time != 0 else 0

        save_results(user, wpm)
        authenticate_user(user, wpm)

    master.destroy()

def save_results(user, wpm):
    results_folder = "User Data"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    results_file = f"{results_folder}/{user}_typing_results.json"
    if os.path.exists(results_file):
        with open(results_file, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(wpm)
    with open(results_file, "w") as file:
        json.dump(data, file)

def authenticate_user(user, new_wpm):
    results_folder = "User Data"
    results_file = f"{results_folder}/{user}_typing_results.json"
    if os.path.exists(results_file):
        with open(results_file, "r") as file:
            data = json.load(file)
        
        if len(data) > 1:
            avg_wpm = sum(data[:-1]) / (len(data) - 1)
            if abs(new_wpm - avg_wpm) <= 5.5:
                print(f"User {user} authenticated.")
            else:
                print(f"User {user} not authenticated. Typing speed significantly different.")    
    else:
            print(f"No previous WPM record found for user {user}. Please type the sentence three times to get a WPM count.")
            get_input(user, sentence_template.format(user=user), repeat=3)
            print(f"Initial data has been registered for user {user}. Please authenticate again.")

def get_user_identity():
    user = input("Enter your username: ")
    
    results_folder = "User Data"
    results_file = f"{results_folder}/{user}_typing_results.json"
    
    if os.path.exists(results_file):
        sentence = sentence_template.format(user=user)
        get_input(user, sentence)
    else:
        authenticate_user(user, 0)

def get_input(user, sentence, repeat=1):
    global master
    master = tk.Tk()
    e = tk.Entry(master)
    e.pack()
    e.bind("<Key>", lambda event: key(event, user))
    
    if repeat > 1:
        e.bind("<Return>", lambda event: repeat_input(event, user, sentence, repeat-1))
    else:
        e.bind("<Return>", lambda event: quit(event, user))
    
    print("___________________________________________")
    print(f"User {user} - TYPE: '{sentence}'")
    master.mainloop()

def repeat_input(event, user, sentence, repeat):
    global master
    master.destroy()
    get_input(user, sentence, repeat)

get_user_identity()
