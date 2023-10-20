import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import uuid
from tkinter import filedialog
from tkinter import Tk

def get_background_color(image_path):
    image = plt.imread(image_path)
    clicked_color = []

    def on_click(event):
        y, x = int(event.ydata), int(event.xdata)
        color = image[y, x, :3]
        clicked_color.append(color)
        plt.close()

    plt.imshow(image)
    plt.axis('off')
    plt.gcf().canvas.mpl_connect('button_press_event', on_click)
    plt.show()
    
    return tuple(int(c * 255) for c in clicked_color[0]) if clicked_color else None

def segment_and_save_sprites(image_path, output_folder, background_color, threshold=50):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image = cv2.imread(image_path)
    distance = np.sqrt(np.sum((image - background_color)**2, axis=-1))
    mask = distance > threshold
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    sprite_count = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 10 or h < 10:
            continue
        sprite = image[y:y+h, x:x+w]
        
        # Generate a random filename using uuid
        random_filename = f"{uuid.uuid4().hex}.png"
        
        output_path = os.path.join(output_folder, random_filename)
        cv2.imwrite(output_path, sprite)
        sprite_count += 1
    return sprite_count

# Initialize Tkinter root window (it won't be shown)
root = Tk()
root.withdraw()

# Open file dialog to select multiple image files
file_paths = filedialog.askopenfilenames(title="Select image files", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

# Loop over each selected file path
for file_path in file_paths:
    background_color = get_background_color(file_path)
    print(f"Selected background color for {file_path}: {background_color}")
    
    output_folder = os.path.join(os.path.dirname(file_path), "images")
    
    sprite_count = segment_and_save_sprites(file_path, output_folder, background_color)
    print(f"Saved {sprite_count} sprites for {file_path}.")

