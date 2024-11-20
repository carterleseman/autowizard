import os
import cv2
import json
import time
import numpy
import pyautogui
import pygetwindow
import pydirectinput

# Suppress OpenCV warnings
cv2.setLogLevel(2)

def cleanup():
    tmp_file = "tmp_resized.png"
    if os.path.exists(tmp_file):
        try:
            os.remove(tmp_file)
            print(f"Removed temporary file '{tmp_file}'")
        except:
            print(f"Error removing '{tmp_file}'")
            wait_for_input()

def wait_for_input(prompt="Press Enter to exit..."):
    # Prevent program from closing instantly on failure
    input(prompt)

def load_config(config_file="config.json"):
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from config file '{config_file}'. Please check the file format.")
        wait_for_input()
        return {}
    except Exception as e:
        print(f"An unexpected error occured while loading the config: {e}")
        wait_for_input()
        return {}

def get_game_window(title="Wizard101"):
    try:
        window = pygetwindow.getWindowsWithTitle(title)[0]
        return window
    except IndexError:
        print(f"No window with title '{title}'.")
        return None

def activate_window(window_title):
    try:
        window = get_game_window(window_title)
        pydirectinput.press('altleft')
        window.activate()
        time.sleep(0.5)
    except AttributeError:
        print(f"Could not move window '{window_title}' to foreground.")

def move_cursor(location, offset_x=0, offset_y=0):
    try:
        x, y = location

        x += offset_x
        y += offset_y
        # Absolute mouse movement
        pydirectinput.moveTo(x, y)
    except TypeError:
        return

def clear_cursor(offset_x=None, offset_y=200):
    # Relative mouse movement
    pydirectinput.move(offset_x, offset_y)

def click(clicks=1, interval=1):
    pydirectinput.click(clicks=clicks, interval=interval)

def spin():
    pydirectinput.keyUp('d')
    pydirectinput.keyDown('d')

def exit_spin():
    pydirectinput.keyUp('d')

def resize_image(image_path, scale_factor):
    try:
        img = cv2.imread(image_path)
        width = int(img.shape[1] * scale_factor)
        height = int(img.shape[0] * scale_factor)
        resized_image = cv2.resize(img, (width, height))
        return resized_image
    except AttributeError:
        return None

def locate_image_with_scaling(img_path, img, screen_region, min_scale=0.5, max_scale=1.5, step=0.1, confidence=0.625 , reverse=False):
    """
    Attempts to locate an image at multiple scales, with optional direction control.
    
    :param img_path: Path to the image to locate.
    :param screen_region: Region of the screen to search within.
    :param min_scale: Minimum scale factor to start resizing.
    :param max_scale: Maximum scale factor to scale the image.
    :param step: Step size for resizing.
    :param confidence: Confidence level for matching the image.
    :param reverse: If True, scales from max_scale to min_scale; otherwise, scales from min_scale to max_scale.
    :return: The location of the image if found, or None if not found.
    """
    error = False

    if reverse:
        scales = numpy.arange(max_scale, min_scale - step, -step) # Reverse range
    else:
        scales = numpy.arange(min_scale, max_scale, step) # Normal range

    for scale in scales:
        # Resize the image
        resized_image = resize_image(img_path, scale)

        if resized_image is None:
            if not error:
                print(f"The image at path '{img_path}' does not exist or could not be loaded.")
                error = True
            continue

        resized_img_path = "tmp_resized.png"
        try:
            cv2.imwrite(resized_img_path, resized_image) # Save resized image temporarily
        except cv2.error:
            continue

        try:
            # Locate the image on screen
            location = pyautogui.locateOnScreen(resized_img_path, region=screen_region, confidence=confidence)

            if location:
                print(f"Found '{img}' at scale {scale:.2f} with confidence {confidence}.")
                return location
            break
        except pyautogui.ImageNotFoundException:
            continue
        except ValueError:
            continue
        
    print(f"Could not find '{img}' at any scale between {min_scale} and {max_scale} with confidence {confidence}.")
    return None

def formulate_center(location):
    try:
        center_x = location.left + location.width // 2
        center_y = location.top + location.height // 2

        center_location = (center_x, center_y)
        return center_location
    except AttributeError: 
        return None

def screenshot(window_title):
    window = get_game_window(window_title)

    if window is None:
        return None
    
    # Get window dimensions
    left, top = window.left, window.top
    width, height = window.width, window.height

    # Capture screenshot within the game window region
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    return screenshot

def detect_combat(window_title):
    screen = screenshot(window_title)
    if screen is None:
        return False
    
    images = ["assets/flee.png", "assets/pass.png"]
    region = (0, 0, screen.width, screen.height)

    for img_path in images:
        location = locate_image_with_scaling(
            img_path,
            img=img_path.split("/")[-1],
            screen_region=region,
            confidence=0.65
        )

        if location:
            return True # Return as soon as one image is found
        
    # If no image is found
    return False

def detect_latency_error(window_title):
    screen = screenshot(window_title)
    if screen is None:
        return False
    
    img_path = "assets/change.png"
    region = (0, 0, screen.width, screen.height)

    location = locate_image_with_scaling(
        img_path,
        img="change.png",
        screen_region=region,
        confidence=0.65
    )

    if location:
        center_location = formulate_center(location)
        move_cursor(center_location)
        click()
        return True
        
    return False

def enchant_available(window_title, enchant_priority):
    screen = screenshot(window_title)
    if screen is None:
        return False

    for enchant in enchant_priority:
        img_path = f"assets/sun/{enchant}.png"
        print(f"Looking for enchant '{enchant}'.")

        region = (0, 0, screen.width, screen.height)
        location = locate_image_with_scaling(img_path, enchant, region, confidence=0.55)

        if location:
            center_location = formulate_center(location)
            move_cursor(center_location)
            
            return True
        
    return False

def use_aura(window_title, aura_priority):
    screen = screenshot(window_title)
    if screen is None:
        return False
    
    for aura in aura_priority:
        print(f"Looking for aura '{aura}'.")
        img_path = f"assets/star/{aura}.png"

        region = (0, 0, screen.width, screen.height)
        location = locate_image_with_scaling(img_path, aura, region, confidence=0.55)

        if location:
            center_location = formulate_center(location)
            move_cursor(center_location)
            click()
            clear_cursor()
            return True

    return False # No aura used

def play_card(window_title, spell_priority, school, enchant_found):
    screen = screenshot(window_title)
    if screen is None:
        return False

    for card in spell_priority:
        print(f"Looking for spell '{card}'.")
        img_path = f"assets/{school}/{card}.png"

        region = (0, 0, screen.width, screen.height)
        location = locate_image_with_scaling(img_path, card, region)

        if location:
            center_location = formulate_center(location)
            if enchant_found:
                click()

                move_cursor(center_location)

                new_location = locate_image_with_scaling(img_path, card, region, min_scale=0.1, max_scale=2.0, reverse=True)
                new_center_location = formulate_center(new_location)

                move_cursor(new_center_location)
                click(clicks=2, interval=0.135)

                time.sleep(1)

                if detect_latency_error(window_title):
                    move_cursor(new_center_location, offset_x=40)
                    click()
            else:
                move_cursor(center_location)
                click()

            return True
        
    return False

def main(config):
    window_title = config.get("window_title", "Wizard101")
    school = config.get("school")
    spell_priority = config.get("spell_priority", {}).get(school, [])
    enchant_priority = config.get("spell_priority", {}).get("sun", [])
    aura_priority = config.get("spell_priority").get("star", [])

    if not spell_priority:
        print(f"No spell priority found for school '{school}'. Check config.")
        wait_for_input()
        return
    
    activate_window(window_title)

    try:
        while True:
            # Step 1: Detect if player is in combat
            if detect_combat(window_title):
                print("In combat!")
                exit_spin()
                
                # Step 2: Search for aura
                if use_aura(window_title, aura_priority):
                    # If aura used, start the loop over
                    continue

                # Step 3: Search for enchantd
                enchant_found = enchant_available(window_title, enchant_priority)

                # Step 4: Apply enchant (if found) and play card
                play_card(window_title, spell_priority, school, enchant_found)

                clear_cursor()
                time.sleep(1)
            else:
                print("Waiting for combat...")
                spin()
                time.sleep(3)  # Wait before checking again
    except KeyboardInterrupt:
        print("Program interrupted. Cleaning up and quitting...")

    finally:
        cleanup()

if __name__ == "__main__":
    config = load_config()

    main(config)