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
    # Wait for the launcher to open
    wait_for_process('WizardLauncher.exe')
    
    for _ in range(10): # Retry for up to 10 seconds
        try:
            app = Application().connect(title="Wizard101", class_name="#32770", backend="win32")
            return app.window(class_name="#32770")
        except Exception:
            time.sleep(1) # Wait before trying again

# Function to get the progress value using ctypes and the HWND (handle of the progress bar)
def get_progress_value(hwnd):
    for _ in range(3): # Retry a few times
        try:
            progress_value = ctypes.windll.user32.SendMessageW(hwnd, PBM_GETPOS, 0, 0)

            if progress_value < 0 or progress_value > 100:
                raise ValueError("Invalid progress value detected.")
            
            return progress_value
        except Exception:
            time.sleep(1) # Wait before retrying

    print("Error retrieving progress bar value.")
    return None # All attempts failed

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
    if ACCOUNT_LOGGING:
        print(f"Logging in to account: {username}")

    # Connect to the Wizard101 launcher
    window = get_launcher_window()

    try:
        username_field = window.child_window(class_name="Edit", found_index=0)
        password_field = window.child_window(class_name="Edit", found_index=1)

        username_field.set_edit_text(username)
        password_field.set_edit_text(password)
    except Exception as e:
        print(f"Error retrieving credential fields: {e}")
        return False

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

def launch_launcher(launcher_path, use_steam=False, steam_path=None):
    executable = steam_path if use_steam else launcher_path
    args = ["-applaunch", "799960"] if use_steam else []
    try:
        if os.path.exists(executable):
            subprocess.Popen([executable] + args)
            return True # Successful launch
        else:
            raise FileNotFoundError(f"Path '{executable}' does not exist.")
    except (Exception, FileNotFoundError) as e:
        print(f"Error launching the game: {e}")
        return False # Launch error

def main(accounts, config):
    launcher_path = config.get("wizard_exe_path")
    steam_path = config.get("steam_exe_path")
    enable_account_selection = config.get("enable_account_selection", False)
    enable_steam = config.get("enable_steam", False)

    print("Please do not interact with the launcher while the script is running.")

    selected_accounts = accounts # Default to logging in all accounts

    # Handle optional account selection if enabled
    if enable_account_selection:
        try:
            selected_indexes = [
                int(i) - 1 for i in input("Enter accounts to log in (e.g., 2 4 to log in to accounts 2 and 4): ").split()
            ]

            if any(i < 0 or i >= len(accounts) for i in selected_indexes):
                raise IndexError

            selected_accounts = [accounts[i] for i in selected_indexes if 0 <= i < len(accounts)] 
        except (ValueError, IndexError):
            print("Invalid account selection.")
            return

    # Handle option steam account selection if enabled
    steam_account = None
    if enable_steam:
        try:
            steam_account_index = int(input(f"Enter the account number to launch through Steam (1-{len(selected_accounts)}): ")) - 1

            if steam_account_index < 0 or steam_account_index >= len(selected_accounts):
                raise IndexError

            steam_account = selected_accounts[steam_account_index] if 0 <= steam_account_index < len(selected_accounts) else None
        except (ValueError, IndexError):
            print("Invalid input for Steam account selection.")
            return

    for account in selected_accounts:
        # Step 1: Launch the Wizard101 launcher or Steam
        if not launch_launcher(launcher_path, use_steam=(account == steam_account), steam_path=steam_path):
            return

        # Step 2: Input the credentials
        if not login_account(*account):
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

    # WARNING: Please manage your account credentials securely
    # Avoid sharing this script with your credentials hardcoded

    # Steam path is for Steam feature usage
    # Account selection is False to login to all accounts by default
    # Steam feature usage is False by default
    config = {
        "wizard_exe_path": r"C:\path\to\Wizard101.exe",
        "steam_exe_path": r"C:\path\to\steam.exe",
        "enable_account_selection": False,
        "enable_steam": False
    }

    main(accounts, config)