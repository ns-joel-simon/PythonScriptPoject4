"""
This Python script monitors internet connection, logs its status,
and records connection history in a JSON file. If the connection
is down, it displays a pop-up alert using a Tkinter GUI."""

import json
import logging
import os
import time
from datetime import datetime
import tkinter as tk
import urllib.request

# Set up logging
log_file = "internet_check.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# JSON file path
json_file = "internet_status.json"


# Function to check internet connection
def check_internet():
    try:
        # Attempt to connect to Google's public DNS server (as a simple connection check)
        urllib.request.urlopen("http://www.google.com", timeout=5)
        return True
    except:
        return False


# Function to update the JSON file and log the result
def update_status():
    internet_status = check_internet()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Log the internet status
    if internet_status:
        logging.info("Internet is UP")
    else:
        logging.info("Internet is DOWN")

    # Update the JSON file
    status_data = {
        "timestamp": timestamp,
        "internet_status": internet_status
    }

    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(status_data)

    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)


# GUI alert if internet is down (using tkinter)
def show_alert():
    if not check_internet():
        root = tk.Tk()
        root.title("Internet Alert")
        root.geometry("300x100")
        label = tk.Label(root, text="Internet is DOWN!", fg="red", font=("Arial", 16))
        label.pack(pady=20)
        root.after(5000, root.destroy)  # Auto-close the window after 5 seconds
        root.mainloop()


if __name__ == "__main__":
    update_status()
    show_alert()  # Optional if you want to use tkinter pop-up for alerts
