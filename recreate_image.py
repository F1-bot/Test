from PIL import Image, ImageDraw, ImageFont

def create_image_v2():
    """
    Generates an image that reproduces the provided sample, with user feedback incorporated.
    - More accurate colors
    - Left-aligned text block
    - Semi-transparent background for each text line
    """
    # Image parameters
    width, height = 1280, 720
    bg_color = "#10101d"
    text_color = "#cccccc"
    quote_bg_color = (0, 0, 0, 51)  # RGBA for black with 20% opacity
    text_lines = [
        'Unfortunately the Haskell type system cannot "prove" that',
        "instances satisfy these laws."
    ]
    output_filename = "reproduced_image.png"
    padding = 15 # Padding for the quote background

    # Create a new image in RGBA mode to support transparency
    image = Image.new("RGBA", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Font selection
    font_size = 40
    font_path = None
    common_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
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

    # --- Layout Calculation ---

    # 1. Get dimensions for all text lines and find the max width
    line_bboxes = [draw.textbbox((0, 0), line, font=font) for line in text_lines]
    line_heights = [bbox[3] - bbox[1] for bbox in line_bboxes]
    max_text_width = max(bbox[2] - bbox[0] for bbox in line_bboxes)

    # 2. Calculate total height of the text block including padding
    total_text_height = sum(line_heights) + (len(text_lines) * padding)

    # 3. Calculate top-left corner for the text block to center it
    start_x = (width - max_text_width) / 2
    start_y = (height - total_text_height) / 2

    current_y = start_y

    # --- Drawing ---

    # Create a separate transparent layer for drawing rectangles and text
    text_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)

    for i, line in enumerate(text_lines):
        line_width = line_bboxes[i][2] - line_bboxes[i][0]
        line_height = line_heights[i]

        # Define the rectangle for the quote background
        rect_x0 = start_x - padding
        rect_y0 = current_y - (padding/2)
        rect_x1 = start_x + max_text_width + padding
        rect_y1 = current_y + line_height + (padding/2)

        # Draw the semi-transparent rectangle
        text_draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=quote_bg_color)

        # Draw the text
        text_draw.text((start_x, current_y), line, font=font, fill=text_color)

        # Update Y position for the next line
        current_y += line_height + padding

    # Composite the text layer onto the main image
    image = Image.alpha_composite(image, text_layer)

    # Save the image
    image.save(output_filename)
    print(f"Image saved as {output_filename}")

if __name__ == "__main__":
    create_image_v2()
