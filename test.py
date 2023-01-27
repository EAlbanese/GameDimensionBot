from PIL import Image, ImageDraw, ImageFont
import requests
import io

# Open the background image
bg_img = Image.open("resources/bg.png")

# Create an ImageDraw object
draw = ImageDraw.Draw(bg_img)

# Define the font and font size
font = ImageFont.truetype("resources/font.ttf", 80)

text = f"Username#0000 just joined the server"

# Draw the text on the background
draw.text((bg_img.width/2-draw.textlength(text, font=font)/2, bg_img.height-325), text,
          font=font, fill=(255, 255, 255))

# Open the image you want to add
avatar_request = requests.get(
    "https://cdn.discordapp.com/avatars/479537494384181248/7c744a1d09c758cf27210de752ddce6a.png?size=256")
avatar_img = Image.open(io.BytesIO(avatar_request.content))
img_pos = (int(bg_img.width/2-avatar_img.width/2), 150)
radius = 256/2

# Create a mask image with rounded corners
mask = Image.new("RGBA", avatar_img.size, (0, 0, 0, 0))
draw_mask = ImageDraw.Draw(mask)
draw_mask.polygon(
    [
        (radius, 0), (avatar_img.width-radius, 0),
        (avatar_img.width-radius, avatar_img.height),
        (radius, avatar_img.height)
    ],
    fill=(255, 255, 255, 255)
)
draw_mask.rectangle(
    [(0, 0), (avatar_img.width, avatar_img.height)],
    fill=(255, 255, 255, 255)
)

# Apply the mask to the original image
avatar_img.paste(mask, (0, 0), mask)

# Paste the image on the background
bg_img.paste(avatar_img, img_pos)

# Save the final image
bg_img.save("final.png")
