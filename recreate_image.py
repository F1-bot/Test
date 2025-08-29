from PIL import Image, ImageDraw, ImageFont

def create_image_for_real_this_time():
    """
    Generates the image with final adjustments for line spacing.
    """
    # Image parameters
    width, height = 1280, 720
    bg_color = "#151723"
    plate_color = "#191925"
    text_color = "#bfc1ce"
    text_lines = [
        'Unfortunately the Haskell type system cannot "prove" that',
        "instances satisfy these laws."
    ]
    output_filename = "reproduced_image.png"
    padding = 10      # Padding within the plates (left/right/top/bottom)
    line_gap = 15       # Extra space between the plates

    # Create a new image in RGB mode
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Font selection
    font_size = 36
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

    # --- Layout Calculation (with Line Gap) ---

    # 1. Get text dimensions
    line_bboxes = [draw.textbbox((0, 0), line, font=font) for line in text_lines]
    line_widths = [bbox[2] - bbox[0] for bbox in line_bboxes]
    line_heights = [bbox[3] - bbox[1] for bbox in line_bboxes]
    max_text_width = max(line_widths)

    # 2. Calculate total height of the block including padding and gaps
    total_plate_height = sum(line_heights) + len(text_lines) * (2 * padding)
    total_gap_height = (len(text_lines) - 1) * line_gap
    total_block_height = total_plate_height + total_gap_height

    # 3. Calculate starting positions
    block_start_x = (width - max_text_width) / 2
    current_y = (height - total_block_height) / 2

    # --- Drawing ---

    for i, line in enumerate(text_lines):
        line_width = line_widths[i]
        line_height = line_heights[i]

        # Define the plate for the current line
        plate_x0 = block_start_x - padding
        plate_y0 = current_y
        plate_x1 = block_start_x + line_width + padding
        plate_y1 = current_y + line_height + (2 * padding)

        draw.rectangle([plate_x0, plate_y0, plate_x1, plate_y1], fill=plate_color)

        # Draw the text, aligned to the block and centered vertically in its plate
        text_x = block_start_x
        text_y = current_y + padding
        draw.text((text_x, text_y), line, font=font, fill=text_color)

        # Update Y for the next plate, including the gap
        current_y += line_height + (2 * padding) + line_gap

    # Save the image
    image.save(output_filename)
    print(f"Image saved as {output_filename}")

if __name__ == "__main__":
    create_image_for_real_this_time()
