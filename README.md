# autowizard

An automated application for opening multiple instances of Wizard101.

## Use Cases
*Boxing* refers to running multiple instances of Wizard101 with different accounts, enabling you to solo PvE battles more effectively.

With autowizard, you can also easily manage tasks like training pets, completing daily assignments, and gardening by automating the login process for each account, eliminating the need to manually open the launcher and enter credentials.

Learn more about boxing on [Final Bastion](https://finalbastion.com/wizard101-guides/quad-boxing-wizard101/#:~:text=Learn%20more%20about%20Quad-Boxing%20in#:~:text=Learn%20more%20about%20Quad-Boxing%20in).

## Features
- **Automated Account Opening**: Open multiple accounts effortlessly.
- **Account Selection**: Choose which accounts to launch.
- **Steam Integration**: Track playtime and display your game status on Steam for one selected account.

While autowizard is designed for multiple instances, it can also be used to open a single account.

<!-- ## Requirements
- **Python**: Make sure Python is installed on your system. You can download it from [Python.org](https://www.python.org/).

autowizard uses libraries like `psutil` and `pywinauto` to automate the Wizard101 launcher's GUI. Non-standard libraries will be automatically installed on the first run using `pip`. -->

## Usage
1. **Ensure** `config.json` **exists** in the same directory/folder as `autowizard.exe`.
2. **Open** `config.json` in a text editor (e.g., Notepad++, VSCode, Notepad) and make the [needed](#1-adding-your-accounts) changes.
3. **Run** `autowizard.exe`.

These sections must be updated for your setup.

### 1. Adding Your Accounts

Add or remove accounts as needed, and replace the placeholders with your actual login credentials:
```json
"accounts": [
    ["username1", "password1"],
    ["username2", "password2"],
    ["username3", "password3"],
    ["username4", "password4"]
]
```

### 2. Setting the Wizard101.exe Path

Specify the path to the `Wizard101.exe` file, ensuring that you use double backslashes:
```json
"wizard_exe_path": "C:\\path\\to\\Wizard101.exe"
```

### *Optional*: Enable Account Selection 

By default, all specified accounts open, but you can change that by enabling this option.

If you want to select which accounts to open (for example, opening only accounts 1 and 3), change `false` to `true`:
```json
"enable_account_selection": true
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
```json
"steam_exe_path": "C:\\path\\to\\steam.exe"
```
3. **Enable Steam Integration**:
Change `"enable_steam"` option from `false` to `true`:
```json
"enable_steam": true
```

*Tip*: If you plan to use one account more frequently, it's recommended to select that account.

### *Optional*: Disable Logging

By default, logging for the progress bar percentage is enabled.

You can turn logging off by changing `true` to `false`:
```json
"progress_logging": false
```

## Final Notes

- **Save Changes**: Ensure that you save your changes to `config.json` before running the script.
- **Check Paths**: Double-check that the paths to `Wizard101.exe` and `steam.exe` are correct.
- It's important that the path to `Wizard101.exe` is to the real one and not a shortcut.

Enjoy your automated Wizard101 experience!

<!-- Compiledd using pyinstaller:
pyinstaller --onefile --clean --noupx --hidden-import=comtypes.stream --version-file=version_info.txt autowizard.py -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.