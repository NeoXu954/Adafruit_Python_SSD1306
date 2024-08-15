import time
import Adafruit_SSD1306
from PIL import Image, ImageSequence

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# 加载GIF文件
gif_path = '/home/neo/dynamic_face.gif'
gif_image = Image.open(gif_path)

# 播放GIF动画的每一帧
while True:
    for frame in ImageSequence.Iterator(gif_image):
        # 转换为1位图像以便显示
        frame = frame.convert('1')
        
        # 调整图像大小以匹配OLED屏幕尺寸
        frame = frame.resize((disp.width, disp.height), Image.ANTIALIAS)
        
        # 显示这一帧
        disp.image(frame)
        disp.display()
        
        # 停顿一下，以便于观察动画效果
        time.sleep(gif_image.info['duration'] / 1000.0)  # 'duration'是每帧的时间间隔，单位为毫秒
        
    # 重新加载GIF以重置帧迭代器
    gif_image.seek(0)
