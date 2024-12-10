from PIL import Image
import base64

def resize_and_encode_image(image_path: str, max_width: int = 800, max_height: int = 800, quality: int = 70) -> str:
    """
    Resizes an image to fit within max dimensions and compresses it.
    Then encodes the resized image into base64.

    Parameters:
        image_path (str): The path to the image.
        max_width (int): The maximum width of the resized image.
        max_height (int): The maximum height of the resized image.
        quality (int): The quality of the output image (1-100).

    Returns:
        str: The base64-encoded string of the resized and compressed image.
    """
    with Image.open(image_path) as img:
        # Resize the image while maintaining aspect ratio
        img.thumbnail((max_width, max_height))
        
        # Save the resized image to a temporary location with reduced quality
        temp_path = "resized_image.jpg"
        img.save(temp_path, format="JPEG", quality=quality)
        
        # Encode the resized image to base64
        with open(temp_path, "rb") as temp_file:
            base64_image = base64.b64encode(temp_file.read()).decode("utf-8")
    
    return base64_image
