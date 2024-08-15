from max30102 import MAX30102, calc_hr_spo2
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

# 初始化 OLED 显示屏
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# 初始化 MAX30102 传感器
sensor = MAX30102()
buff_size = 100
ir_data = []
red_data = []
bpms = []
spo2s = []

# 主循环
try:
    while True:
        num_bytes = sensor.get_data_present()
        if num_bytes > 0:
            while num_bytes > 0:
                red, ir = sensor.read_fifo()
                num_bytes -= 1
                ir_data.append(ir)
                red_data.append(red)

                # 维持缓冲区大小
                while len(ir_data) > buff_size:
                    ir_data.pop(0)
                    red_data.pop(0)

        # 当缓冲区满时进行计算
        if len(ir_data) == buff_size:
            hr_valid, hr, spo2_valid, spo2 = calc_hr_spo2(ir_data, red_data)
            if hr_valid and spo2_valid:
                bpms.append(hr)
                spo2s.append(spo2)

            while len(bpms) > 4:
                bpms.pop(0)
                spo2s.pop(0)

            hr_mean = np.mean(bpms)
            spo2_mean = np.mean(spo2s)

            # 在 OLED 显示屏上显示结果
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((0, 0), f'HR: {hr_mean:.2f} BPM', font=font, fill=255)
            draw.text((0, 15), f'SpO2: {spo2_mean:.2f}%', font=font, fill=255)
            disp.image(image)
            disp.display()

        time.sleep(1)

except KeyboardInterrupt:
    print('程序中断')

finally:
    disp.clear()
    disp.display()
    sensor.shutdown()

