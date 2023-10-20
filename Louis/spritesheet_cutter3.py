# Import required libraries
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

def get_background_color(image_path):
    """
    Display an image and allow the user to click on it.
    Return the RGB color of the clicked pixel.
    """
    # Load the image using Matplotlib's imread function
    image = plt.imread(image_path)
    
    # Initialize an empty list to store the clicked color
    clicked_color = []

    # Define a function that will be called when the image is clicked
    def on_click(event):
        # Get the coordinates of the clicked point
        y, x = int(event.ydata), int(event.xdata)
        
        # Get RGB color at the clicked point
        color = image[y, x, :3]
        
        # Append the color to the clicked_color list
        clicked_color.append(color)
        
        # Close the displayed image window
        plt.close()

    # Display the image using Matplotlib
    plt.imshow(image)
    
    # Remove axis
    plt.axis('off')
    
    # Attach the click event to the displayed image
    plt.gcf().canvas.mpl_connect('button_press_event', on_click)
    
    # Show the image
    plt.show()
    
    # Return the clicked color, convert to RGB values in the range [0, 255]
    return tuple(int(c * 255) for c in clicked_color[0]) if clicked_color else None

def segment_and_save_sprites(image_path, output_folder, background_color, threshold=50):
    """
    Segment sprites based on background color and save them.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # Calculate the Euclidean distance between each pixel and the background color
    distance = np.sqrt(np.sum((image - background_color)**2, axis=-1))
    
    # Create a binary mask where the distance is greater than a threshold
    mask = distance > threshold

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize a counter for the saved sprites
    sprite_count = 0
    
    # Loop over each detected contour
    for contour in contours:
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Skip small noise artifacts
        if w < 10 or h < 10:
            continue
        
        # Extract the sprite from the original image
        sprite = image[y:y+h, x:x+w]
        
        # Construct the output path for the sprite
        output_path = os.path.join(output_folder, f"sprite_{sprite_count}.png")
        
        # Save the sprite using OpenCV
        cv2.imwrite(output_path, sprite)
        
        # Increment the sprite counter
        sprite_count += 1

    # Return the total number of saved sprites
    return sprite_count

# Get the background color from the user by displaying the image and allowing a click
background_color = get_background_color("sprites.png")
print(f"Selected background color: {background_color}")

# Segment the sprites from the original image and save them to a folder
sprite_count = segment_and_save_sprites(
    "sprites.png",  # Source image
    "./images",  # Output folder
    background_color  # Background color to segment against
)
print(f"Saved {sprite_count} sprites.")

