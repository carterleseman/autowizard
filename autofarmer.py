import os
import cv2
import json
import time
import numpy
import pyautogui
import pygetwindow

def cleanup():
    tmp_file = "tmp_resized.png"
    if os.path.exists(tmp_file):
        try:
            os.remove(tmp_file)
            print(f"Removed temporary file '{tmp_file}'")
        except:
            print(f"Error removing '{tmp_file}'")
            wait_for_input()

def wait_for_input():
    # Prevent program from closing instantly on failure
    input("Press Enter to exit...")

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
    window = pygetwindow.getWindowsWithTitle(title)[0]
    if not window:
        print(f"Window '{title}' not found.")
        return None
    return window

def activate_window(window_title):
    window = get_game_window(window_title)

    window.activate()
    time.sleep(0.5)

def move_cursor(location):
    pyautogui.moveTo(location)

def click(clicks=1, interval=1):
    pyautogui.mouseDown()
    pyautogui.click(clicks=clicks, interval=interval)
    time.sleep(0.5)
    pyautogui.mouseUp()

def resize_image(image_path, scale_factor):
    img = cv2.imread(image_path)
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)
    resized_image = cv2.resize(img, (width, height))
    return resized_image

def locate_image_with_scaling(img_path, img, screen_region, min_scale=0.5, max_scale=1.5, step=0.1, confidence=0.625):
    """
    Attempts to locate an image at multiple scales (from min_scale to max_scale).
    
    :param img_path: Path to the image to locate.
    :param screen_region: Region of the screen to search within.
    :param min_scale: Minimum scale factor to start resizing.
    :param max_scale: Maximum scale factor to scale the image.
    :param step: Step size for resizing.
    :param confidence: Confidence level for matching the image.
    :return: The location of the image if found, or None if not found.
    """
    for scale in numpy.arange(min_scale, max_scale, step):
        # Resize the image
        resized_image = resize_image(img_path, scale)
        resized_img_path = "tmp_resized.png"
        cv2.imwrite(resized_img_path, resized_image) # Save resized image temporarily

        try:
            # Locate the image on screen
            location = pyautogui.locateOnScreen(resized_img_path, region=screen_region, confidence=confidence)

            if location:
                print(f"Found '{img}' at scale {scale:.2f} with confidence {confidence}")
                return location
            break
        except pyautogui.ImageNotFoundException:
            continue
        
    print(f"Could not find '{img}' at any scale between {min_scale} and {max_scale} with confidence {confidence}")
    return None

def formulate_center(location):
    center_x = location.left + location.width // 2
    center_y = location.top + location.height // 2

    center_location = (center_x, center_y)
    return center_location

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
    
    region = (0, 0, screen.width, screen.height)
    location = locate_image_with_scaling("assets/pass.png", "pass button", region, min_scale=0.5, max_scale=1.5, step=0.1, confidence=0.7)
    return location is not None

# def get_playable_cards(window_title, spell_priority, school):
#     playable_cards = []

#     screen = screenshot(window_title)
#     if screen is None:
#         return []
    
#     for card in spell_priority:
#         img_path = f"assets/{school}/{card}.png"
        
#         region = (0, 0, screen.width, screen.height)
#         if locate_image_with_scaling(img_path, card, region) is not None:
#             playable_cards.append(card)

#     return playable_cards   

def enchant_available(window_title, enchant_priority):
    screen = screenshot(window_title)
    if screen is None:
        return False

    for enchant in enchant_priority:
        img_path = f"assets/sun/{enchant}.png"
        print(f"Looking for enchant '{enchant}'")

        # Define the region to search
        region = (0, 0, screen.width, screen.height)
        location = locate_image_with_scaling(img_path, enchant, region, confidence=0.55)

        if location:
            center_location = formulate_center(location)
            move_cursor(center_location)
            
            return True
        
    return False

def play_card(window_title, spell_priority, school, enchant_found):
    screen = screenshot(window_title)
    if screen is None:
        return False

    for card in spell_priority:
        # if card not in playable_cards:
        #     print(f"Skipping '{card}' because it's not usable.")
        #     continue

        print(f"Looking for spell '{card}'")
        img_path = f"assets/{school}/{card}.png"

        region = (0, 0, screen.width, screen.height)
        location = locate_image_with_scaling(img_path, card, region)

        if location:
            center_location = formulate_center(location)
            if enchant_found:
                click()

                move_cursor(center_location)

                new_location = locate_image_with_scaling(img_path, card, region, max_scale=2.0)
                new_center_location = formulate_center(new_location)

                move_cursor(new_center_location)
                click(clicks=2, interval=0.15)
            else:
                move_cursor(center_location)
                click()

            return True
        
    return False

def main(config):
    window_title = config.get("window_title", "Wizard101")
    school = config.get("school")
    spell_priority = config.get("spell_priority", {})[school]
    enchant_priority = config.get("spell_priority", {})["sun"]

    activate_window(window_title)

    try:
        while True:
            if detect_combat(window_title):
                print("In combat!")

                # playable_cards = get_playable_cards(window_title, spell_priority, school)

                enchant_found = enchant_available(window_title, enchant_priority)

                play_card(window_title, spell_priority, school, enchant_found)

                time.sleep(1)
            else:
                print("Waiting for combat...")
                time.sleep(5)  # Wait before checking again
    except KeyboardInterrupt:
        print("Program interrupted. Cleaning up and quitting...")

    finally:
        cleanup()

if __name__ == "__main__":
    config = load_config()
    
    main(config)