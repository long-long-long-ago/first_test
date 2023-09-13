import base64
import json
import re
from io import BytesIO
from PIL import Image

import ddddocr

chromedriver_url = "../msedgedriver"
now_url = "https://ah.91huayi.com"


def readQues():
    with open('ques.json', 'r', encoding='utf-8') as file:
        quesStr = file.read()
        quesrtion_dir = json.loads(quesStr)
        print(quesrtion_dir)
        print(type(quesrtion_dir))
        return quesrtion_dir


# 识别数字验证码
def shibieyanzhengma():
    ocr = ddddocr.DdddOcr()
    with open('../WebDriver/xx.png', 'rb') as f:
        img_bytes = f.read()
    yzm = ocr.classification(img_bytes)
    print(yzm)
    return yzm


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    try:
        img = Image.open(image_data)
    except:
        print("-----")
    return img
