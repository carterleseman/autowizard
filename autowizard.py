import os
import json
import time
import ctypes
import warnings
import subprocess

def load_config(config_file="config.json"):
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found.")
        wait_for_input()
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from config file '{config_file}'. Please check the file format.")
        wait_for_input()
        return {}
    except Exception as e:
        print(f"An unexpected error occured while loading the config: {e}")
        wait_for_input()
        return {}

import psutil
import win32gui
import pygetwindow
from pywinauto import Application

# Suppress 32-bit application automated using 64-bit Python warning
warnings.filterwarnings("ignore", category=UserWarning, module="pywinauto.application")

PBM_GETPOS = 0x0408  # Message to get the current progress bar position
SPI_GETWORKAREA = 0x0030

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

def wait_for_input():
    # Prevent program from closing instantly on failure
    input("Press Enter to exit...")

def get_screen_resolution():
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    return screen_width, screen_height

def get_taskbar_height():
    desktop = ctypes.wintypes.RECT()

    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(desktop), 0)

    _, screen_height = get_screen_resolution()

    # Taskbar height is the difference between screen height and the working area bottom
    taskbar_height = screen_height - desktop.bottom

    return taskbar_height

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

def wait_for_progress_complete(config):
    # Connect to the Wizard101 Launcher
    window = get_launcher_window()

    progress_bar = window.child_window(class_name="msctls_progress32", found_index=1)

    while True:
        progress = get_progress_value(progress_bar)

        if progress is None:
            print("Progress retrieval failed. Possibly incorrect credentials.")
            return False # Exit; Login failed

        if config.get("progress_logging", True):
            print(f"Progress: {progress}%")

        # Check if progress bar is complete (100%)
        if progress == 100:
            break

        time.sleep(1)
    
    return True # Login was successful

def select_accounts(accounts):
    print("Available accounts:")
    for idx, account in enumerate(accounts, 1):
        print(f"{idx}: {account[0]}")

    try:
        selected_indexes = [
            int(i) - 1 for i in input("Enter account numbers to log in (e.g., 1 2 3): ").split()
        ]

        # Validate
        if any(i < 0 or i >= len(accounts) for i in selected_indexes):
            raise IndexError
        
        return [accounts[i] for i in selected_indexes]
    except (ValueError, IndexError):
        print("Invalid account selection(s).")
        wait_for_input()
        return None # Invalid selection(s)
    
def select_steam_account(selected_accounts):
    print("Available accounts:")
    for idx, account in enumerate(selected_accounts, 1):
        print(f"{idx}: {account[0]}")

    print("Enter 'skip' to bypass Steam login.")

    try:
        user_input = input(f"Enter the account number to launch through Steam or 'skip': ").strip().lower()

        if user_input == 'skip' or user_input == '':
            print("Skipping Steam login.")
            return None # Skip Steam login
        
        steam_account_index = int(user_input) - 1

        if steam_account_index < 0 or steam_account_index >= len(selected_accounts):
            raise IndexError
    
        return selected_accounts[steam_account_index]
    except (ValueError, IndexError):
        print("Invalid input for Steam account selection")
        wait_for_input()
        return None # Invalid selection
    
def login_account(username, password, config):
    print(f"Logging in to account '{username}'")

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

    if not wait_for_progress_complete(config):
        print(f"Login failed for account '{username}'. Skipping to the next account.")
        close_process('WizardLauncher.exe')
        # Wait a bit after closing launcher to prevent errors
        wait_for_process('WizardLauncher.exe', False)
        return False # Failure

    play_button = window.child_window(title="PLAY!", class_name="Button")
    play_button.click()

    print(f"Successfully logged in to account '{username}'")

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
        wait_for_input()
        return False # Launch error
    
def position_game_window(window_positions, username, index):
    positions = window_positions[index % len(window_positions)]

    screen_width, screen_height = get_screen_resolution()
    taskbar_height = get_taskbar_height()

    window = pygetwindow.getWindowsWithTitle("Wizard101")[0]

    window_width = window.width
    window_height = window.height

    x, y = positions
    if x == screen_width:
        x -= window_width
    if y == screen_height:
        y -= (window_height + taskbar_height)

    print(f"Moving window for account '{username}' to position ({x}, {y})")
    win32gui.MoveWindow(window._hWnd, x, y, window_width, window_height, True)

    # print(f"Renaming window for account '{username}'")
    win32gui.SetWindowText(window._hWnd, username)

def main(accounts, config):
    launcher_path = config.get("wizard_exe_path")
    steam_path = config.get("steam_exe_path")
    enable_account_selection = config.get("enable_account_selection", False)
    enable_steam = config.get("enable_steam", False)
    enable_window_positioning = config.get("enable_window_positioning", True)
    window_positions = config.get("window_positions", [(0, 0)])

    print("Please do not interact with the launcher while the script is running.")

    selected_accounts = accounts

    # Handle optional account selection if enabled
    if enable_account_selection:
        selected_accounts = select_accounts(accounts)
        if selected_accounts is None:
            return  

    steam_account = None

    # Handle option steam account selection if enabled
    if enable_steam:
        steam_account = select_steam_account(selected_accounts)

    for idx, account in enumerate(selected_accounts):
        # Step 1: Launch the Wizard101 launcher or Steam
        if not launch_launcher(launcher_path, use_steam=(account == steam_account), steam_path=steam_path):
            return

        # Step 2: Input the credentials
        if not login_account(*account, config):
            continue

        # Step 3: Wait for the launcher to close
        wait_for_process('WizardLauncher.exe', False)

        # Step 4: Wait until the game client is running
        wait_for_process('WizardGraphicalClient.exe')

        # Step 5: Position game window if enabled
        if enable_window_positioning:
            position_game_window(window_positions, account[0], idx)

if __name__ == "__main__":
    config = load_config()

    accounts = config.get("accounts", [])

    main(accounts, config)