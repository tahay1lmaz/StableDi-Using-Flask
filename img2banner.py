from PIL import Image, ImageDraw, ImageFont

def create_dynamic_ad_template(image_path, logo_path, color_hex, punchline, button_text, output_path):
    # Open the image
    new_image = Image.open(image_path).convert("RGBA")
    
    new_image = new_image.resize((256,256), Image.LANCZOS)
    
    base_image = Image.new("RGBA", (512, 512), "white")
    
 # Paste the original image onto the new image
    base_image.paste(new_image, (128, 128), new_image)

    # Open the logo image
    logo = Image.open(logo_path).convert("RGBA")

    # Resize the logo to fit the template
    logo = logo.resize((150, 100), Image.LANCZOS)

    # Paste the logo at the top center of the base image
    base_image.paste(logo, ((base_image.width - logo.width) // 2, 10), logo)

    # Create a drawing object
    draw = ImageDraw.Draw(base_image)

    # Choose a font and size for punchline
    punchline_font = ImageFont.truetype("arial.ttf", 24)
    
    # Calculate the position for the punchline (centered)
    text_width, text_height = ImageDraw.Draw(base_image).textsize(punchline, punchline_font)

    # Draw the punchline on the image
    draw.text(((base_image.width-text_width)//2, 395), punchline, fill=color_hex, font=punchline_font)
    
    # Choose a font and size for the button text
    button_font = ImageFont.truetype("arial.ttf", 24)
    
    button_text_w, button_text_h = ImageDraw.Draw(base_image).textsize(button_text, button_font)
    
    button_width = button_text_w + 40
    button_height = button_text_h + 20
    button_x = (base_image.width - button_width) // 2
    button_y = 430
    
    draw.rectangle([button_x, button_y, button_x + button_width, button_y + button_height], fill=color_hex)
    
    yazı_x = button_x + (button_width - button_text_w) // 2
    yazı_y = button_y + (button_height - button_text_h) // 2
    
    # button_text_pos = ((base_image.width-button_width)//2,440)
    button_text_font = ImageFont.truetype("arial.ttf", 24)
    draw.text((yazı_x, yazı_y), button_text, fill='white', font=button_text_font)
    
    base_image.save(output_path, "PNG")
