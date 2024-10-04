import os
import sys
import time
import ctypes
import warnings
import subprocess

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_and_install_dependencies():
    required_packages = ['psutil', 'pywinauto']

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing...")
            install(package)
            print(f"{package} has been installed.")

check_and_install_dependencies()

import psutil
from pywinauto import Application

# Suppress 32-bit application automated using 64-bit Python warning
warnings.filterwarnings("ignore", category=UserWarning, module="pywinauto.application")

PBM_GETPOS = 0x0408  # Message to get the current progress bar position
ACCOUNT_LOGGING = True
PROGRESS_LOGGING = True

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def close_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            proc.terminate()
            return

def wait_for_process(process_name, open=True):
    while (is_process_running(process_name)) != open:
        time.sleep(1)

def get_launcher_window():
    app = Application().connect(title="Wizard101", class_name="#32770", backend="win32")
    window = app.window(class_name="#32770")
    return window

# Function to get the progress value using ctypes and the HWND (handle of the progress bar)
def get_progress_value(hwnd):
    try:
        progress_value = ctypes.windll.user32.SendMessageW(hwnd, PBM_GETPOS, 0, 0)

        if progress_value < 0 or progress_value > 100:
            raise ValueError("Invalid progress value detected.")
        
        return progress_value
    except Exception as e:
        # Handle any ctypes or message call errors
        # print(f"Error retrieving progress bar value: {e}")
        return None

def wait_for_progress_complete():
    # Connect to the Wizard101 Launcher
    window = get_launcher_window()
    progress_bar = window.child_window(class_name="msctls_progress32", found_index=1)

    while True:
        progress = get_progress_value(progress_bar)

        if progress is None:
            print("Progress retrieval failed. Possibly incorrect credentials.")
            return False # Exit; Login failed

        if PROGRESS_LOGGING:
            print(f"Progress: {progress}%")

        # Check if progress bar is complete (100%)
        if progress == 100:
            break

        time.sleep(1)
    
    return True # Login was successful

def login_account(username, password):
    # Wait for the launcher to load
    wait_for_process('WizardBrowser.exe')

    if ACCOUNT_LOGGING:
        print(f"Logging in to account: {username}")

    # Connect to the Wizard101 launcher
    window = get_launcher_window()

    username_field = window.child_window(class_name="Edit", found_index=0)
    password_field = window.child_window(class_name="Edit", found_index=1)

    username_field.set_edit_text(username)
    password_field.set_edit_text(password)

    login_button = window.child_window(title="Login", class_name="Button")
    login_button.click()

    if not wait_for_progress_complete():
        print(f"Login failed for account: {username}. Skipping to the next account.")
        close_process('WizardLauncher.exe')
        # Wait a bit after closing launcher to prevent errors
        wait_for_process('WizardLauncher.exe', False)
        return False # Failure

    play_button = window.child_window(title="PLAY!", class_name="Button")
    play_button.click()

    return True # Success

def launch_launcher(launcher_path):
    try:
        if os.path.exists(launcher_path):
            subprocess.Popen(launcher_path)
        else:
            raise FileNotFoundError(f"Launcher path '{launcher_path}' does not exist.")
    except Exception as e:
        print(f"Error launching the game: {e}")

def main(accounts, launcher_path, enable_account_selection=False):
    print("Please do not interact with the launcher while the script is running.")

    # Handle optional account selection
    if enable_account_selection:
        account_selection = input("Enter accounts to login (e.g., 2 4 to log in to accounts 2 and 4): ").split()

        try:
            selected_indexes = [int(index) - 1 for index in account_selection] # Convert to 0-based index
        except ValueError:
            print("Invalid input. Please enter valid account numbers.")
            return
        
        selected_accounts = [(accounts[i][0], accounts[i][1]) for i in selected_indexes if 0 <= i < len(accounts)]

        if not selected_accounts:
            print("No valid accounts selected.")
            return
    else:
        selected_accounts = accounts # Log into all accounts by default

    for username, password in selected_accounts:
        # Step 1: Launch the Wizard101 launcher
        launch_launcher(launcher_path)

        # Step 2: Input the credentials
        if not login_account(username, password):
            continue

        # Step 3: Wait for the launcher to close
        wait_for_process('WizardLauncher.exe', False)

        # Step 4: Wait until the game client is running
        wait_for_process('WizardGraphicalClient.exe')

if __name__ == "__main__":
    # List of accounts in (username, password) format
    accounts = [
        ('username1', 'password1'),
        ('username2', 'password2'),
        ('username3', 'password3'),
        ('username4', 'password4')
    ]

    # Path to your Wizard101 launcher executable
    launcher_path = r"C:\path\to\Wizard101.exe"

    # By default, this is False to log into all accounts
    # To enable account selection, pass True
    main(accounts, launcher_path, enable_account_selection=False)