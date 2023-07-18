import time
import re
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import json

now_url= "https://www.zjzx.ah.cn/"
# chromedriver下载地址：http://chromedriver.storage.googleapis.com/index.html
chromedriver_url = "C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver"
user_name = "340828199102230149"
user_pwd = "230149"

def startPlay(driver):
    driver.switch_to.window(driver.window_handles[1])
    while 1 :
        try:
            js = " let video = document.querySelector('video'); video.playbackRate = 4;"
            base64_str = driver.execute_script(js)
            print(base64_str)
            time.sleep(10)
            endElement = driver.find_element(By.CLASS_NAME, "s - clr - main")
            print(endElement.text)
        except Exception :
            print(Exception)

    pass

def readQues():
    with open('ques.json', 'r' ,encoding='utf-8') as file:
        quesStr = file.read()
        quesrtion_dir = json.loads(quesStr)
        print(quesrtion_dir)
        print(type(quesrtion_dir))
        return quesrtion_dir


def submit(quesrtion_dir):
    print("over")
    submit = driver.find_element(By.CLASS_NAME, "ap-paper-num-p2")
    submit.click()
    checkDialog(False)
    time.sleep(10)
    checkAnswerElement = driver.find_element(By.PARTIAL_LINK_TEXT, "查看试卷")
    checkAnswerElement.click()
    time.sleep(5)
    checkAnswer(driver,quesrtion_dir)
    pass

def checkDialog(i):
    dialogs = driver.find_elements(By.CLASS_NAME, "el-dialog__wrapper")
    for dialog in dialogs:
        if dialog.is_displayed():
            if i :
                dialog.find_element(By.CLASS_NAME, "el-button--default").click()
            else:
                dialog.find_element(By.CLASS_NAME, "el-button--primary").click()

def startExam(driver):
    quesrtion_dir = readQues()
    driver.switch_to.window(driver.window_handles[1])
    checkDialog(True)
    nextQue = driver.find_element(By.PARTIAL_LINK_TEXT, "下一题")
    upQue = driver.find_element(By.CLASS_NAME, "page-prev")
    while True:
        startAnswer(driver,quesrtion_dir)
        if nextQue.is_displayed():
            nextQue.click()
        else:
            submit(quesrtion_dir)
            break
    pass


def saveAnswer(quesrtion_dir):
    with open('ques.json', 'w' ,encoding='utf-8') as file:
        file.write(json.dumps(quesrtion_dir,indent=2))
    pass


def checkAnswer(driver,quesrtion_dir):
    nextQue = driver.find_element(By.PARTIAL_LINK_TEXT, "下一题")
    while True:
        quesDetails = driver.find_element(By.CLASS_NAME,"ap-paper-ques-details")
        quesText = quesDetails.find_element(By.TAG_NAME,"span").text.replace("(","").replace(")","").replace("（","").replace("）","")
        answerTextCode = quesDetails.find_element(By.CLASS_NAME,"ap-paper-ques-ture").find_element(By.TAG_NAME,"span").text
        answertext = ""
        for que in quesDetails.find_elements(By.CLASS_NAME,"ap-paper-ques-abc"):
            if answerTextCode.find(que.text[0]) != -1:
                answertext = answertext + que.text[2:]
        quesrtion_dir[quesText] = answertext
        if nextQue.is_displayed():
            nextQue.click()
        else:
            break
    print(quesrtion_dir)
    saveAnswer(quesrtion_dir)
    pass

def startAnswer(driver,quesrtion_dir):
    quesDetails = driver.find_element(By.CLASS_NAME,"ap-paper-ques-details")
    quesText = quesDetails.find_element(By.TAG_NAME,"span").text.replace("(","").replace(")","").replace("（","").replace("）","")

    answer = getAnswer(quesrtion_dir,quesText)
    ques = quesDetails.find_elements(By.CLASS_NAME,"ap-paper-ques-abc")
    if answer == None:
        ques[0].click()
        answer= "aaa"
    for que in ques:
        if answer.find(que.text[2:]) != -1:
            que.click()

def getAnswer(quesrtion_dir,que):
    return quesrtion_dir.get(que)

def inputCoursePage(driver):
    print("开始等待")
    time.sleep(10)

    loginNameElement = driver.find_element(By.PARTIAL_LINK_TEXT, "进入学习中心")
    # loginNameElement = driver.find_element(By.PARTIAL_LINK_TEXT, "学习中心")
    #
    loginNameElement.click()
    time.sleep(5)
    endElement = driver.find_element(By.CLASS_NAME, "td1")
    if endElement.text.startswith("已"):
        driver.find_element(By.PARTIAL_LINK_TEXT, "去考试").click()
        time.sleep(5)
        startExam(driver)
    else:
        startElement = driver.find_element(By.PARTIAL_LINK_TEXT, "去学习")
        startElement.click()
        time.sleep(2)
        startPlay(driver)
    pass


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # 这个是绝对路径
    driver = webdriver.Chrome(executable_path=chromedriver_url, options=options)
    driver.get(now_url)
    # 最大化浏览器
    driver.maximize_window()
    time.sleep(10)
    loginNameElement = driver.find_element(By.CLASS_NAME, "inp1")
    loginNameElement.send_keys(user_name)
    loginPwdElement = driver.find_element(By.CLASS_NAME, "inp2")
    loginPwdElement.send_keys(user_pwd)
    agreeElement = driver.find_element(By.CLASS_NAME, "btn1")
    agreeElement.click()
    inputCoursePage(driver)


    

