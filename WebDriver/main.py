import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import ddddocr
import pymysql
import base64
import os
import re
from io import BytesIO
from PIL import Image
from WebDriver.Course import Course
import json



now_url = "https://cme23.91huayi.com/pages/course.aspx?cid=6a4543e4-cd7d-4c25-877a-598f46598034&dept_id=8834a9b2-6e44-49ea-acf7-9b8a00f2802b"

# 数据库工具
# db = pymysql.connect(host='localhost', user='root', password='qwer', port=3306, db="jijiao")
# chromedriver地址
chromedriver_url = "C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver"
# user_name = "240572AMR"
# user_name = "240572AAI"
# user_name = "240572ALD"
# user_pwd = "wcd123456"
# 朱乐军
# user_name = "240572AJ9"
# user_name = "24057PAAV" #胡小凤
# user_name = "240572AGB"
# user_name = "240572ADW"
# user_pwd = "yxj123456"
# 定义选项字典，默认null
# user_name="240572AHQ"#黄曙光
# user_name = "240571AJ4" #朱玲莉
# user_pwd = "000000"
# user_name = "240572AJ7"#刘辉
# user_pwd = "lh123456"
user_name = "240571AJ4"#王荣
user_pwd = "000000"
quesrtion_dir = {}

def runJs(driver):
    time.sleep(10*60)
    js = "showExam(true);"
    driver.execute_script(js)


def startwebdriver():
    options = webdriver.ChromeOptions()
    # 这个是绝对路径
    driver = webdriver.Chrome(executable_path=chromedriver_url, options=options)
    driver.get(now_url)
    # 最大化浏览器
    driver.maximize_window()
    loginNameElement = driver.find_element(By.ID, "loginName")
    loginNameElement.send_keys(user_name)
    loginPwdElement = driver.find_element(By.ID, "loginPwd")
    loginPwdElement.send_keys(user_pwd)
    # 识别验证码
    yzmImgElement = driver.find_element(By.ID, "imgCheckCode")
    src= yzmImgElement.get_attribute("src")
    print(src)
    time.sleep(1)
    saveYzm(driver)
    # 写入验证码
    yzmTextElement = driver.find_element(By.ID, "txtCheckCode")
    yzmText = shibieyanzhengma()
    yzmTextElement.send_keys(yzmText)
    # 同意隐私
    agreeElement = driver.find_element(By.ID, "agree")
    agreeElement.click()
    # 登录，跳转到内部页面
    agreeElement = driver.find_element(By.ID, "butLogin")
    agreeElement.click()
    time.sleep(2)
    # ----------------------------------
    # 进入课程列表页面
    switchToCoursePage(driver)
    # ----------------------------------
    time.sleep(3000)
    print("程序关闭")
    driver.close()

#
# def insertMsg(question, answer):
#     cursor = db.cursor()
#     sql = "insert into questions(question,answer) values (%s,%s)"
#     try:
#         cursor.execute(sql, (question, answer))
#         db.commit()
#     except Exception as a:
#         print(a)
#         db.rollback()
#     db.close()


def response_interceptor(request, response):
    t=response.headers['Content-Type']
    print("------------")
    if 'image/Gif' in t:
        print(request.url)
        with open(request.url, 'wb') as f:
            f.write(response.body)


# 保存验证码
def saveYzm(driver):
    js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
         "let img = document.getElementById('imgCheckCode'); /*找到图片*/ " \
         "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
         "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
         "let base64String = c.toDataURL();return base64String;"

    base64_str = driver.execute_script(js)
    print("----------")
    img = base64_to_image(base64_str)
    img.save('xx.png')


#启动webdriver
def switchToCoursePage(driver):
    for win in driver.window_handles:
        driver.switch_to.window(win)
        # print(driver.)
        course = driver.find_elements(By.CLASS_NAME,"f14blue")
        print(len(course))
        current_courses =[]
        is_played = False #判断当前课程是否已经学过了
        # 便利课程列表，选择播放哪一个课程
        for i in range(1, len(course)):
            # print(course[i].text+":"+course[i].get_attribute("href"))
            if course[i].text != "" :
                if(not is_played):
                    # 获取课程链接
                    current_course = Course(course[i].text,course[i].get_attribute("href"))
                    print(current_course.name+":"+current_course.href)
                    current_courses.append(current_course)
            else:
                # print(course[i].find_element(By.TAG_NAME,"img").get_attribute("src").endswith("anniu_03a.gif"))
                if(course[i].find_element(By.TAG_NAME,"img").get_attribute("src").endswith("anniu_03a.gif")):
                    # 已经学习过了，不再学习
                    is_played = True
                else:
                    is_played = False

        if len(current_courses) > 0 :
            for c in current_courses:
                # 跳转到播放页面
                driver.get(c.href)
                swithPalyCoursePage(driver)
            # driver.get(current_courses[3].href)
            # swithPalyCoursePage(driver)


# 进入考试页面
def swithExamCoursePage(driver):
    time.sleep(5)
    quesrtion_id = "gvQuestion_question_"
    driver.switch_to.window(driver.current_window_handle)
    # 共5道题，以此便利
    for i in range(0, 6):
        time.sleep(3)
        # 获取问题内容
        quesrtion_text = driver.find_element(By.ID, quesrtion_id + str(i))

        if quesrtion_dir.get(quesrtion_text.text[2:].replace(" ", "")) is None:
            # 若此道题未写入答案，默认设置A
            quesrtion_dir[quesrtion_text.text[2:].replace(" ", "")] = 1
        print(quesrtion_text.text[2:].replace(" ", ""))
        print(quesrtion_dir.get(quesrtion_text.text[2:].replace(" ", "")))
        # 获取到所有的选项
        answer = driver.find_element(By.ID, "gvQuestion_rbl_" + str(i))
        # print(answer.text)
        answer_labels = answer.find_elements(By.XPATH, ".//label")
        if quesrtion_dir.get(quesrtion_text.text[2:].replace(" ", "")) == 1:
            # 选择答案  A
            answer_labels[0].click()
        elif quesrtion_dir.get(quesrtion_text.text[2:].replace(" ", "")) == 2:
            # 选择答案   B
             answer_labels[1].click()
        elif quesrtion_dir.get(quesrtion_text.text[2:].replace(" ", "")) == 3:
            # 选择答案   C
             answer_labels[2].click()
        elif quesrtion_dir.get(quesrtion_text.text[2:].replace(" ", "")) == 4:
            # 选择答案   D
             answer_labels[3].click()
        elif quesrtion_dir.get(quesrtion_text.text[2:].replace(" ", "")) == 5:
            # 选择答案  E
             answer_labels[4].click()
        else:
            # 选择答案  A
            answer_labels[1].click()

    submit = driver.find_element(By.ID,"btn_submit")
    time.sleep(5)
    submit.click()
    swithChangeAnser(driver)


        # questions =
        # break


def swithChangeAnser(driver):
    try:
        time.sleep(5)
        driver.switch_to.window(driver.current_window_handle)
        # 获取错误题
        dds = driver.find_elements(By.CLASS_NAME, "state_lis_text")
        # dds = left.find_elements_by_xpath(".//dd")
        print("============错误题===========")
        for dd in dds:
            print(dd.get_attribute("title").replace(" ", ""))
            print(str(quesrtion_dir).replace(" ", ""))
            print(dd.get_attribute("title").replace(" ", "") + ":" + str(quesrtion_dir.get(dd.get_attribute("title").replace(" ", ""))))
            quesrtion_dir[dd.get_attribute("title").replace(" ", "")] = quesrtion_dir.get(dd.get_attribute("title").replace(" ", ""))+1
        # 重新考试
        time.sleep(5)
        print("==========================")
        exam_angin = driver.find_elements(By.CLASS_NAME, "state_foot_btn")
        exam_angin[1].click()
        swithExamCoursePage(driver)
    except Exception as e:
        print(e)
        print("恭喜你，考试通过！")
        # 保存答案
        saveAnswer(quesrtion_dir)
        print(str(quesrtion_dir))
        pass

def saveAnswer(quesrtion_dir):
    with open('ques.json', 'w' ,encoding='utf-8') as file:
        file.write(json.dumps(quesrtion_dir,indent=2))
    pass
def runJs1(driver):
    js = "let video = document.querySelector('video');  video.currentTime = video.duration; closeBangZhu();"
    driver.execute_script(js)
    pass

def runJS(driver,js_str):
    driver.execute_script(js_str)

def swithPalyCoursePage(driver):
    buttonClass = "pv-playpause"
    for win in driver.window_handles:
        driver.switch_to.window(win)
        time.sleep(5)
        try:
            print("=====pv-playpause======")
            controls = driver.find_element(By.CLASS_NAME,"pv-controls-left")
            button = controls.find_element(By.XPATH,".//button")
            print("开始播放")
            button.click()
        except NoSuchElementException as e:
            print(e)
            print("=====此页面采用H5播放器，已开始自动播放======")
            # button = driver.find_element_by_id("ccH5TogglePlay")
        # 自动播放

        # 等待进入考试按钮出现href
        print(driver.current_url)
        jrksElemente = driver.find_element(By.ID, "jrks")
        jrksHref = "#"
        while jrksHref[-1] == "#":
            # 没有看完，继续等待十分钟
            print("开始等待十秒钟......")
            time.sleep(10)
            runJs1(driver)
            jrksHref = jrksElemente.get_attribute("href")
            runJS(driver,"closeBangZhu()")
        print(jrksHref[-1])
        # div_processbar_tip 无法跳跃提示框

        jrksElemente.click()
        swithExamCoursePage(driver)
        break


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img


def gif_to_png():
    im = Image.open('../CheckCode.jpg')
    transparency = im.info['transparency']
    im.save('test1.png', transparency=transparency)
    # print(im.tell())
    # im.seek(im.tell())
    # transparency = im.info['transparency']
    # im.save('test2.png', transparency=transparency)


#识别数字验证码
def shibieyanzhengma():
    ocr = ddddocr.DdddOcr()
    with open('../WebDriver/xx.png', 'rb') as f:
        img_bytes = f.read()
    yzm = ocr.classification(img_bytes)
    print(yzm)
    return yzm

def readQues():
    with open('ques.json', 'r' ,encoding='utf-8') as file:
        quesStr = file.read()
        quesrtion_dir = json.loads(quesStr)
        print(quesrtion_dir)
        print(type(quesrtion_dir))
        return quesrtion_dir



if __name__ == '__main__':
    # 获取题目答案
    quesrtion_dir = readQues()
    startwebdriver()