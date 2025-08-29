from PIL import Image, ImageDraw, ImageFont

def create_image():
    """
    Generates an image that reproduces the provided sample.
    """
    # Image parameters
    width, height = 1280, 720
    bg_color = "#202124"  # A dark blue-gray
    text_color = "#D1D1D1" # A light gray
    text_lines = [
        'Unfortunately the Haskell type system cannot "prove" that',
        "instances satisfy these laws."
    ]
    output_filename = "reproduced_image.png"

    # Create a new image with the specified background color
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Font selection
    font_size = 40
    font_path = None
    common_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "C:/Windows/Fonts/Arial.ttf",                      # Windows
        "/System/Library/Fonts/Supplemental/Arial.ttf",    # macOS
    ]

    for f_path in common_fonts:
        try:
            font = ImageFont.truetype(f_path, font_size)
            font_path = f_path
            break
        except IOError:
            continue

    if not font_path:
        print("Could not find a common system font. Using default font.")
        font = ImageFont.load_default()

    # Calculate text size and position
    # The anchor 'mm' means the text is centered horizontally and vertically at the given coordinate.
    x, y = width / 2, height / 2

    # We need to calculate the total height of the text block to center it vertically.
    total_text_height = 0
    line_heights = []
    for line in text_lines:
        try:
            # Use getbbox for more accurate size calculation
            bbox = draw.textbbox((0, 0), line, font=font)
            line_height = bbox[3] - bbox[1]
        except AttributeError:
            # Fallback for older Pillow versions
            line_width, line_height = draw.textsize(line, font=font)

        total_text_height += line_height
        line_heights.append(line_height)

    # Calculate starting y position
    current_y = y - (total_text_height / 2)

    # Draw each line of text
    for i, line in enumerate(text_lines):
        # Center each line horizontally
        line_y = current_y + (line_heights[i] / 2)
        draw.text((x, line_y), line, font=font, fill=text_color, anchor="mm")
        current_y += line_heights[i]


    # Save the image
    image.save(output_filename)
    print(f"Image saved as {output_filename}")

if __name__ == "__main__":
    create_image()
