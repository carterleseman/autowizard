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
- **Window Positioning**: Automatically position windows based on screen coordinates.

> [!NOTE]
> While autowizard is designed for multiple instances, it can also be used to open a single account.

## Usage
1. **Ensure** `config.json` **exists** in the same directory/folder as `autowizard.exe`.
2. **Open** `config.json` in a text editor (e.g., Notepad++, VSCode, Notepad) and make the [needed](#1-adding-your-accounts) changes.
3. **Run** `autowizard.exe`.

> [!IMPORTANT]
> The following sections must be updated for your setup.

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

> [!NOTE]
> This integration is for a single account only. It does not support running multiple instances using different Steam accounts.

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

> [!TIP]
> If you plan to use one account more frequently, it's recommended to select that account.

### *Optional*: Disable Logging

By default, logging for the progress bar percentage is enabled.

You can turn logging off by changing `true` to `false`:
```json
"progress_logging": false
```

### *Optional*: Window Positioning

This feature allows you to control where each window opens on your screen.

By default, window positioning is enabled. You can specify multiple positions for the windows, and each account will open in the corresponding spot on your screen.

You can set up the `window_positions` config to define where each game window will be placed. Positions are specified as [x, y] coordinates relative to your screen's top left corner.
```json
"window_positions": [
    [0, 0],
    [1920, 0],
    [0, 1080],
    [1920, 1080]
]
```

I've included coordinates based on a 1920x1080 screen resolution. Change these coordinates to fit your own.

If you have more accounts than positions, the process will cycle back through the positions.
 - You have 1 account and 4 specified positions. It will use the first position.
 - You have 4 accounts and 2 specified positions. It will use the 2 positions and then cycle back through for the last 2 accounts.
 - You have 4 accounts and 0 specified positions. All accounts will use [0, 0].

# autofarmer

An automated application designed to assist players with farming in Wizard101 using image recognition.

## Use Cases
*Farming* in autofarmer's case refers to repeatedly engaging in battles to collect gold, reagents, seeds (like couch potatoes), or other valuable drops in Wizard101.

autofarmer is best suited for simplifying repetitive mob fights, where battles require minimal strategy and can be automated effectively. It's ideal for running the tool overnight or while you're away.

> [!NOTE]  
> autofarmer is an active process and cannot run in the background. The game must remain open and active during use.

## Features
- **Customizable Spell Priorities**: Tailor the spell list to match your character's deck.
- **Dynamic Spell Selection**: Skips to the next spell if a higher-priority one isn't available.
- **Enchantment & Aura Selection**: Use of buffs to enhance your character's damage output.

## Usage
1. **Ensure** `config.json` **exists** in the same directory/folder as `autofarmer.exe`.
2. **Open** `config.json` in a text editor (e.g., Notepad++, VSCode, Notepad) and make the [needed](#1-wizard101-window-title) changes.
3. **Ensure** Wizard101 is running.
3. **Run** `autofarmer.exe`.

> [!TIP]
> autofarmer works best on higher resolutions. For the absolutely best results, put your game on borderless.

### 1. Wizard101 Window Title

By default, autofarmer targets the active game window titled **"Wizard101"**. However, if **window positioning** is enabled, you must set `window_title` to match the username of the account logged in and farming.

Example Configuration:
```json
"accounts": [
    ["username1", "password1"]
],
"enable_window_positioning": true,
"window_title": "username1"
```

This ensures autofarmer correctly identifies the game window when positioning is enabled.

### 2. School and Spell Priorities

Ensure your school is correctly set:
```json
"school": "storm"
```

This ensures autofarmer looks for spells relevant to your character.

Spell priorities should reflect your deck setup. Place the most frequently used or important spells at the start of the list. autofarmer reads priorities from left (highest priority) to right (lowest priority). If there are spells you are not going to use, remove them altogether for quicker results.

Example configuration:
```json
"spell_priority": {
    "sun": ["epic"],
    "star": [],
    "storm": ["bunyips_rage", "tempest"]
}
```

If a spell isn't found during battle, autofarmer automatically skips to the next one.

## Possible Misconceptions

- **Single Account/Instance**: autofarmer does not support multiple instances.
- **Active Use Only**: The game must remain the active window. autofarmer cannot function in the background.
- **Simple Battles Only**: autofarmer is designed for basic mob farming, not complex boss fights or PvP scenarios.

# Final Notes

- **Save Changes**: Make sure to save your changes to `config.json` before running the program.
- **Check Paths**: Double-check that the paths to `Wizard101.exe` and `steam.exe` are correct. They should point to the actual executable files, not shortcuts.

> [!CAUTION]
> Treat your `config.json` file like sensitive information. Don't share it with others to avoid risking your login credentials.

Enjoy your automated Wizard101 experience!

<!-- Compiled using pyinstaller:
pyinstaller --onefile --clean --noupx --hidden-import=comtypes.stream --version-file=autowizard_version.txt --icon=autowizard.ico autowizard.py -->

<!-- Compiled using pyinstaller:
pyinstaller --onefile --clean --noupx --hidden-import=comtypes.stream --version-file=autofarmer_version.txt --icon=autofarmer.ico autofarmer.py -->

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.