import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw
import speech_recognition as sr

# 初始化OLED显示屏
RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height

def draw_face(mood,frame):
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    
    # 通用的眼睛位置
    eye_center = (width // 4, height // 3)
    eye_size = 8
    
    # 绘制眼睛
    draw.ellipse((eye_center[0] - eye_size, eye_center[1] - eye_size, 
                  eye_center[0] + eye_size, eye_center[1] + eye_size), outline=255, fill=255)
    draw.ellipse((width - eye_center[0] - eye_size, eye_center[1] - eye_size, 
                  width - eye_center[0] + eye_size, eye_center[1] + eye_size), outline=255, fill=255)

    # 根据情绪绘制嘴巴
    mouth_center = (width // 2, height * 2 // 3)
    mouth_width = 40
    mouth_height = 16
    '''
    if mood == 'happy':
        # 动态高兴表情（嘴角上扬）
        smile_height = 16 + (frame % 5)  # 嘴角随帧数变化
        draw.arc((mouth_center[0] - mouth_width // 2, mouth_center[1] - smile_height // 2,
                  mouth_center[0] + mouth_width // 2, mouth_center[1] + smile_height // 2), start=0, end=180, fill=255)

    elif mood == 'sad':
        # 动态难过表情（嘴角下垂）
        sad_height = 16 + (frame % 5)  # 嘴角随帧数变化
        draw.arc((mouth_center[0] - mouth_width // 2, mouth_center[1] - sad_height // 2,
                  mouth_center[0] + mouth_width // 2, mouth_center[1]), start=0, end=-180, fill=255)
        # 添加眼泪
        tear_y = eye_center[1] + eye_size + (frame % 5) * 3
        draw.ellipse((eye_center[0] - 2, tear_y, eye_center[0] + 2, tear_y + 4), outline=255, fill=255)

    else:
        # 默认表情
        draw.line((mouth_center[0] - mouth_width // 2, mouth_center[1],
                   mouth_center[0] + mouth_width // 2, mouth_center[1]), fill=255)

    disp.image(image)
    disp.display()
    '''
    if mood == 'happy':
        # 更大幅度的动态高兴表情（嘴角上扬）
        smile_height = 16 + ((frame % 10) * 2)  # 增加变化范围
        draw.arc((mouth_center[0] - mouth_width // 2, mouth_center[1] - smile_height // 2,
                  mouth_center[0] + mouth_width // 2, mouth_center[1] + smile_height // 2), start=0, end=180, fill=255)

    elif mood == 'sad':
        # 动态难过表情（嘴角下垂）
        sad_height = 16 + ((frame % 10) * 2)  # 增加变化范围
        # 绘制向下的弧线
        draw.arc((mouth_center[0] - mouth_width // 2, mouth_center[1] - sad_height // 2,
              mouth_center[0] + mouth_width // 2, mouth_center[1]), start=180, end=0, fill=255)
        # 添加眼泪
        tear_y = eye_center[1] + eye_size + ((frame % 10) * 3)  # 增加眼泪的移动速度
        draw.ellipse((eye_center[0] - 2, tear_y, eye_center[0] + 2, tear_y + 4), outline=255, fill=255)


    else:
        # 默认表情
        draw.line((mouth_center[0] - mouth_width // 2, mouth_center[1],
                   mouth_center[0] + mouth_width // 2, mouth_center[1]), fill=255)

    disp.image(image)
    disp.display()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='zh-CN')
            print("您说: " + text)
            return text
        except sr.UnknownValueError:
            print("Google 语音识别无法理解音频")
        except sr.RequestError as e:
            print("无法从Google 语音识别服务请求结果; {0}".format(e))

    return ""

# 表情关键词字典
face_keywords = {
    'happy': ["笑", "开心"],
    'sad': ["哭", "难过"]
}


# 设置初始表情
current_mood = 'default'
frame = 0
draw_face(current_mood, frame)  # 在这里也传递frame参数


# 主循环
try:
    while True:
        speech_text = recognize_speech()
        
        # 更新当前情绪
        for mood, keywords in face_keywords.items():
            if any(keyword in speech_text for keyword in keywords):
                if current_mood != mood:
                    current_mood = mood
                break
        else:
            if current_mood != 'default':
                current_mood = 'default'

        # 绘制当前表情的当前帧
        draw_face(current_mood, frame)
        frame += 1
        
        #time.sleep(0.5)  # 更新动画的速度
        time.sleep(0.2)  # 减少睡眠时间以加快动画速度

except KeyboardInterrupt:
    disp.clear()
    disp.display()
    print("程序已停止")
