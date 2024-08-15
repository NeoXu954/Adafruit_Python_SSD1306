import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Define constants to draw the face
eye_center_y = height // 4
eye_center_x_left = width // 4
eye_center_x_right = width * 3 // 4
eye_size = 8  # Reduced eye size

# Define mouth properties
mouth_center = (width // 2, height // 2)  # Adjusted mouth center
mouth_width = 40  # Increased mouth width
mouth_height = 8  # Decreased mouth height

# Duration of one blink cycle in seconds
blink_duration = 2
blink_time = 0.2

# Start main loop
while True:
    # Clear the image buffer
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw eyes open
    draw.ellipse((eye_center_x_left - eye_size, eye_center_y - eye_size,
                  eye_center_x_left + eye_size, eye_center_y + eye_size), outline=255, fill=255)
    draw.ellipse((eye_center_x_right - eye_size, eye_center_y - eye_size,
                  eye_center_x_right + eye_size, eye_center_y + eye_size), outline=255, fill=255)
    
    # Draw mouth
    draw.ellipse((mouth_center[0] - mouth_width // 2, mouth_center[1] - mouth_height // 2,
                  mouth_center[0] + mouth_width // 2, mouth_center[1] + mouth_height // 2), outline=255, fill=0)

    # Display image on the screen
    disp.image(image)
    disp.display()
    
    # Pause for blink duration
    time.sleep(blink_duration - blink_time)
    
    # Clear the image buffer for eyes closed
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw mouth again for eyes closed (since we cleared the buffer)
    draw.ellipse((mouth_center[0] - mouth_width // 2, mouth_center[1] - mouth_height // 2,
                  mouth_center[0] + mouth_width // 2, mouth_center[1] + mouth_height // 2), outline=255, fill=0)

    # Display image on the screen
    disp.image(image)
    disp.display()
    
    # Pause for blink time
    time.sleep(blink_time)
