# autowizard

An automated script for opening multiple instances of Wizard101.

## Use Cases
*Boxing* refers to running multiple instances of Wizard101 with different accounts, enabling you to solo PvE battles more effectively.

With autowizard, you can also easily manage tasks like training pets, completing daily assignments, and gardening by automating the login process for each account, eliminating the need to manually open the launcher and enter credentials.

Learn more about boxing on [Final Bastion](https://finalbastion.com/wizard101-guides/quad-boxing-wizard101/#:~:text=Learn%20more%20about%20Quad-Boxing%20in#:~:text=Learn%20more%20about%20Quad-Boxing%20in).

## Features
- **Automated Account Opening**: Open multiple accounts effortlessly.
- **Account Selection**: Choose which accounts to launch.
- **Steam Integration**: Track playtime and display your game status on Steam for one selected account.

While autowizard is designed for multiple instances, it can also be used to open a single account.

## Requirements
- **Python**: Make sure Python is installed on your system. You can download it from [Python.org](https://www.python.org/).

autowizard uses libraries like `psutil` and `pywinauto` to automate the Wizard101 launcher's GUI. Non-standard libraries will be automatically installed on the first run using `pip`.

## Usage
1. **Open** `autowizard.py` in a text editor (e.g., Notepad++, VSCode, Notepad).
2. **Scroll to the bottom of the file** (lines 202-220).

These sections must be updated for your setup.

### 1. Adding Your Accounts

Add or remove accounts as needed, and replace the placeholders with your actual login credentials:
```
accounts = [
        ('username1', 'password1'),
        ('username2', 'password2'),
        ('username3', 'password3'),
        ('username4', 'password4')
    ]
```

### 2. Setting the Wizard101.exe Path

Specify the path to the `Wizard101.exe` file:
```
wizard_exe_path = r"C:\path\to\Wizard101.exe"
```

### *Optional*: Enable Account Selection 

If you want to select which accounts to open (for example, opening only accounts 1 and 3), change `False` to `True`:
```
"enable_account_selection": True
```

### *Optional*: Steam Integration

*Please note that this integration does not allow you to run multiple instances using separate Steam accounts. It is only for tracking playtime or displaying your game status.*

This feature is primarily intended for users who want to track their playtime or let friends know they are playing Wizard101 through Steam, while using the original launcher.

To integrate the original Wizard101 with Steam, follow these steps:
1. **Set Launcher Options in Steam**:
In the steam properties for Wizard101, set the launch options to:
```
"C:\path\to\Wizard101.exe" %command%
```
2. **Specify the path to `steam.exe`**:
Set the path to the Steam executable:
```
"steam_path_exe": r"C:\path\to\steam.exe"
```
3. **Enable Steam Integration**:
Change `"enable_steam"` option from `False` to `True`:
```
"enable_steam": True
```

*Tip*: If you plan to use one account more frequently, it's recommended to select that account.

## Final Notes

Make sure to save your changes before running the script. Enjoy your automated Wizard101 experience!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.