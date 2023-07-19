import time
import re
import traceback
from io import BytesIO
from PIL import Image

from WebDriver import Properties
from selenium import webdriver

from selenium.webdriver.common.by import By
import ddddocr
import pymysql
import base64
import json

now_url= "https://ah.91huayi.com"


class_1_url = "https://ah.91huayi.com/train/courseware/list?cid=E3352E80-B575-4E64-8B67-2468A3221821&mid=7876BF64-EFE0-E811-A088-005056A62382"
class_2_url = "https://ah.91huayi.com/train/courseware/list?cid=9B604FD7-3841-4584-989F-568E5D972C84&mid=7876BF64-EFE0-E811-A088-005056A62382"
class_3_url = "https://ah.91huayi.com/train/courseware/list?cid=8DC68B06-2DB7-4262-AABB-C96A40633D40C&mid=7876BF64-EFE0-E811-A088-005056A62382"
class_4_url = "https://ah.91huayi.com/train/courseware/list?cid=AA19A88E-CE8B-4D88-AC5C-7CD07D7D72E5&mid=7876BF64-EFE0-E811-A088-005056A62382"
chromedriver_url = "C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver"

# 定义选项字典，默认null
quesrtion_dir = {}
# 保存验证码
def saveYzm(driver):
    js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
         "let img = document.getElementsByName('codeimg')[0]; /*找到图片*/ " \
         "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
         "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
         "let base64String = c.toDataURL();return base64String;"

    base64_str = driver.execute_script(js)
    print(base64_str)
    img = base64_to_image(base64_str)
    img.save('xx.png')


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    try:
        img = Image.open(image_data)
    except :
        print("-----")
    return img


def switchToCoursePage(driver,class_url):
    # 跳转到播放页面
    driver.get(class_url)
    time.sleep(5)
    content_box = driver.find_elements(By.XPATH,"//*[@id='listBox']/ div / ul / li")
    print(len(content_box))
    courses = []
    for content in content_box:
        course = content.find_element(By.TAG_NAME,"a")
        courses.append(course.get_attribute("href"))
    for course in courses:
        print("开始学习："+ course)
        swithPalyCoursePage(driver, course)
    # swithPalyCoursePage(driver, courses[4])

def readQues():
    with open('ques.json', 'r' ,encoding='utf-8') as file:
        quesStr = file.read()
        quesrtion_dir = json.loads(quesStr)
        print(quesrtion_dir)
        print(type(quesrtion_dir))
        return quesrtion_dir


def swithExamCoursePage(driver):
    time.sleep(1)
    driver.switch_to.window(driver.current_window_handle)

    # 共5道题，以此便利
    kaoshi_box = driver.find_element(By.CLASS_NAME,"kaoshi_box")
    shitis = kaoshi_box.find_elements(By.CLASS_NAME,"shiti")
    for shiti in shitis:
        time.sleep(1)
        # 获取问题内容
        quesrtion_text = shiti.find_element(By.TAG_NAME,"p").text[2:].replace(" ", "").replace("<","")
        # daan = quesrtion_dirs.get(quesrtion_text)
        print(quesrtion_text)
        if quesrtion_dir.get(quesrtion_text) is None :
            # 若此道题未写入答案，默认设置A
            quesrtion_dir[quesrtion_text] = 1
        # 答案
        print(quesrtion_dir.get(quesrtion_text))
        # 获取到所有的选项
        answers = shiti.find_elements(By.TAG_NAME,"li")
        for answer in answers:
            print(answer.find_element(By.TAG_NAME,"span").text)
        if quesrtion_dir.get(quesrtion_text) == 1 :
            # 选择答案  A
            answers[0].find_element(By.TAG_NAME,"input").click()
        elif quesrtion_dir.get(quesrtion_text) == 2:
            # 选择答案  B
            answers[1].find_element(By.TAG_NAME,"input").click()
        elif quesrtion_dir.get(quesrtion_text) == 3:
            # 选择答案  C
            answers[2].find_element(By.TAG_NAME,"input").click()
        elif quesrtion_dir.get(quesrtion_text) == 4:
            # 选择答案  D
            answers[3].find_element(By.TAG_NAME,"input").click()
        elif quesrtion_dir.get(quesrtion_text) == 5 :
            # 选择答案  E
            answers[4].find_element(By.TAG_NAME,"input").click()
        else:
            answers[0].find_element(By.TAG_NAME,"input").click()
    #
    submit = driver.find_element(By.CLASS_NAME,"but2_a")
    time.sleep(5)
    submit.click()
    swithChangeAnser(driver)

    time.sleep(10)


def swithChangeAnser(driver):
    try:
        time.sleep(5)
        driver.switch_to.window(driver.current_window_handle)
        # 获取错误题
        left = driver.find_element(By.CLASS_NAME,"kj_f_box")
        dds = left.find_elements(By.XPATH,".//ul/li")
        print("============错误题===========")
        for dd in dds:
            print(str(dd.text[2:]).replace(" ", "").replace("&lt;",""))
            quesrtion_dir[dd.text[2:].replace(" ", "").replace("&lt;","")] = quesrtion_dir.get(dd.text[2:].replace(" ", "").replace("&lt;",""))+1
        # 重新考试
        time.sleep(10)
        print("==========================")
        exam_angin_box = driver.find_element(By.CLASS_NAME,"but3")
        exam_angin = exam_angin_box.find_elements(By.TAG_NAME,"button")[1]
        exam_angin.click()
        swithExamCoursePage(driver)
    except Exception as e:
        print(e)
        print('\n','>>>'*20)
        print(traceback.print_exc())
        print("恭喜你，考试通过！")
        print("=========正确答案=============")
        print(str(quesrtion_dir))
        # 保存答案
        saveAnswer(quesrtion_dir)
        print("============================")
        pass

def saveAnswer(quesrtion_dir):
    with open('ques.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(quesrtion_dir, ensure_ascii=False, indent=2))
    pass



def swithPalyCoursePage(driver, course_href):
    driver.get(course_href)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)
    beisuJS1(driver)
    # lis = driver.find_element(By.CLASS_NAME,"list_kc2").find_elements(By.CLASS_NAME,"li")
    # ccH5TogglePause = driver.find_element(By.CLASS_NAME,"ccH5TogglePlay")
    # ccH5TogglePause.click()
    time.sleep(10)
    # 进入考试按钮
    jrksElemente = driver.find_element(By.ID, "jrks")
    jrksHref = "#"
    while jrksHref == None or jrksHref[-1] == "#":
        # 没有看完，继续等待十分钟
        print("开始等待十分钟......")
        time.sleep(10)
        jrksHref = jrksElemente.get_attribute("href")
    print(jrksHref[-1])
    jrksElemente.click()
    swithExamCoursePage(driver)
    time.sleep(8)


def startwebdriver():
    options = webdriver.ChromeOptions()
    # 这个是绝对路径
    driver = webdriver.Chrome(executable_path=chromedriver_url, options=options)
    driver.get(now_url)
    # 最大化浏览器
    driver.maximize_window()
    loginNameElement = driver.find_element(By.NAME, "user_name")
    loginNameElement.send_keys(Properties.user_name)
    loginPwdElement = driver.find_element(By.NAME, "password")
    loginPwdElement.send_keys(Properties.user_pwd)
    # 识别验证码
    yzmImgElement = driver.find_element(By.NAME, "codeimg")
    src= yzmImgElement.get_attribute("src")
    print(src)
    time.sleep(1)
    saveYzm(driver)
    # 写入验证码
    yzmTextElement = driver.find_element(By.NAME, "code")
    yzmText = shibieyanzhengma()
    yzmTextElement.send_keys(yzmText)
    # 同意隐私
    agreeElement = driver.find_element(By.ID, "ckAgreement")
    agreeElement.click()
    # 登录，跳转到内部页面
    agreeElement = driver.find_element(By.CLASS_NAME, "login")
    agreeElement.click()
    time.sleep(2)
    # ----------------------------------
    # 进入课程列表页面
    # 播放第一个视频
    switchToCoursePage(driver,class_1_url)
    # switchToCoursePage(driver, class_2_url)
    # switchToCoursePage(driver, class_3_url)
    # 播放第四个视频
    # switchToCoursePage(driver, class_4_url)
    # ----------------------------------
    time.sleep(30)
    print("程序关闭")
    driver.close()


# 5倍速
def beisuJS(driver):
    js = " let video = document.querySelector('video');" \
         "function play() {" \
         "video.playbackRate = 5;}"\
         "    setInterval(play, 100);"
    base64_str = driver.execute_script(js)
    pass

def playVideo(driver):
    js = " let video = document.querySelector('video');" \
         "video.play()"
    driver.execute_script(js)
    pass

def beisuJS1(driver):
    js = "course_ware_finish()"
    driver.execute_script(js)



#识别数字验证码
def shibieyanzhengma():
    ocr = ddddocr.DdddOcr()
    with open('../WebDriver/xx.png', 'rb') as f:
        img_bytes = f.read()
    yzm = ocr.classification(img_bytes)
    print(yzm)
    return yzm

if __name__ == '__main__':
    # 获取题目答案
    quesrtion_dir = readQues()
    startwebdriver()
