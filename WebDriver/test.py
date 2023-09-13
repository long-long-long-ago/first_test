import json
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By

from WebDriver import Utils, Properties

# 获取题目答案
quesrtion_dir = Utils.readQues()
tjkcs_list = []


def run():
    startwebdriver()


def startwebdriver():
    # options = webdriver.ChromeOptions()
    options = webdriver.EdgeOptions()
    # 这个是绝对路径
    driver = webdriver.Chrome(executable_path=Utils.chromedriver_url, options=options)
    driver.get(Utils.now_url)
    # 最大化浏览器
    driver.maximize_window()
    loginNameElement = driver.find_element(By.NAME, "user_name")
    loginNameElement.send_keys(Properties.user_name)
    loginPwdElement = driver.find_element(By.NAME, "password")
    loginPwdElement.send_keys(Properties.user_pwd)

    yzmImgElement = driver.find_element(By.NAME, "codeimg")
    src = yzmImgElement.get_attribute("src")
    print(src)
    time.sleep(1)
    saveYzm(driver)
    # 写入验证码
    yzmTextElement = driver.find_element(By.NAME, "code")
    yzmText = Utils.shibieyanzhengma()
    yzmTextElement.send_keys(yzmText)
    # 同意隐私
    agreeElement = driver.find_element(By.ID, "ckAgreement")
    agreeElement.click()
    # 登录，跳转到内部页面
    agreeElement = driver.find_element(By.CLASS_NAME, "login")
    agreeElement.click()
    time.sleep(2)
    # ----------------------------------
    # 遍历titleList获取所有类型
    titleList = driver.find_element(By.ID, "titleList")
    titles = titleList.find_elements(By.TAG_NAME, "li")
    for title in titles:
        # 分别进入临床、护理、医技、药学、公共卫生、中医药大类
        title.click()
        time.sleep(5)
        while True:
            tjkc_list = driver.find_element(By.CLASS_NAME, "tjkc_list")
            tjkcs = tjkc_list.find_elements(By.TAG_NAME, "a")
            for tjkc in tjkcs:
                class_url = tjkc.get_attribute("href")
                tjkcs_list.append(class_url)
            # 遍历每一页
            try:
                next_page = driver.find_element(By.LINK_TEXT, "下一页")
            except Exception as e:
                break
            next_page_class_name = str(next_page.get_attribute("class"))
            print(next_page_class_name)
            if next_page_class_name == "nextbtn":
                next_page.click()
                time.sleep(5)
    print(tjkcs_list)
    for tjkc in tjkcs_list:
        switchToCoursePage(driver,tjkc)
    # ----------------------------------
    time.sleep(30)
    print("程序关闭")
    driver.close()


# 保存验证码
def saveYzm(driver):
    js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
         "let img = document.getElementsByName('codeimg')[0]; /*找到图片*/ " \
         "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
         "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
         "let base64String = c.toDataURL();return base64String;"

    base64_str = driver.execute_script(js)
    print(base64_str)
    img = Utils.base64_to_image(base64_str)
    img.save('xx.png')


def switchToCoursePage(driver, class_url):
    # 跳转到播放页面
    driver.get(class_url)
    time.sleep(5)
    content_box = driver.find_elements(By.XPATH, "//*[@id='listBox']/ div / ul / li")
    print(len(content_box))
    courses = []
    for content in content_box:
        is_not_play_over = "学习完毕" != content.find_element(By.TAG_NAME, "span").text
        if is_not_play_over:
            course = content.find_element(By.TAG_NAME, "a")
            courses.append(course.get_attribute("href"))
    for course in courses:
        print("开始学习：" + course)
        swithPalyCoursePage(driver, course)
    # swithPalyCoursePage(driver, courses[4])


def swithPalyCoursePage(driver, course_href):
    driver.get(course_href)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)
    beisuJS1(driver)
    playVideo(driver)
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


def beisuJS1(driver):
    js = "course_ware_finish()"
    driver.execute_script(js)


def playVideo(driver):
    js = " let video = document.querySelector('video');" \
         "video.play()"
    driver.execute_script(js)


def swithExamCoursePage(driver):
    time.sleep(1)
    driver.switch_to.window(driver.current_window_handle)

    # 共5道题，以此便利
    kaoshi_box = driver.find_element(By.CLASS_NAME, "kaoshi_box")
    shitis = kaoshi_box.find_elements(By.CLASS_NAME, "shiti")
    for shiti in shitis:
        time.sleep(1)
        # 获取问题内容
        quesrtion_text = shiti.find_element(By.TAG_NAME, "p").text[2:].replace(" ", "").replace("<", "")
        # daan = quesrtion_dirs.get(quesrtion_text)
        print(quesrtion_text)
        if quesrtion_dir.get(quesrtion_text) is None:
            # 若此道题未写入答案，默认设置A
            quesrtion_dir[quesrtion_text] = 1
        # 答案
        print(quesrtion_dir.get(quesrtion_text))
        # 获取到所有的选项
        answers = shiti.find_elements(By.TAG_NAME, "li")
        for answer in answers:
            print(answer.find_element(By.TAG_NAME, "span").text)
        if quesrtion_dir.get(quesrtion_text) == 1:
            # 选择答案  A
            answers[0].find_element(By.TAG_NAME, "input").click()
        elif quesrtion_dir.get(quesrtion_text) == 2:
            # 选择答案  B
            answers[1].find_element(By.TAG_NAME, "input").click()
        elif quesrtion_dir.get(quesrtion_text) == 3:
            # 选择答案  C
            answers[2].find_element(By.TAG_NAME, "input").click()
        elif quesrtion_dir.get(quesrtion_text) == 4:
            # 选择答案  D
            answers[3].find_element(By.TAG_NAME, "input").click()
        elif quesrtion_dir.get(quesrtion_text) == 5:
            # 选择答案  E
            answers[4].find_element(By.TAG_NAME, "input").click()
        else:
            quesrtion_dir[quesrtion_text] = 1
            answers[0].find_element(By.TAG_NAME, "input").click()
    #
    submit = driver.find_element(By.CLASS_NAME, "but2_a")
    time.sleep(2)
    submit.click()
    swithChangeAnser(driver)
    time.sleep(3)


def swithChangeAnser(driver):
    try:
        time.sleep(5)
        driver.switch_to.window(driver.current_window_handle)
        # 获取错误题
        left = driver.find_element(By.CLASS_NAME, "kj_f_box")
        dds = left.find_elements(By.XPATH, ".//ul/li")
        print("============错误题===========")
        for dd in dds:
            print(str(dd.text[2:]).replace(" ", "").replace("&lt;", ""))
            quesrtion_dir[dd.text[2:].replace(" ", "").replace("&lt;", "")] = quesrtion_dir.get(
                dd.text[2:].replace(" ", "").replace("&lt;", "")) + 1
        # 重新考试
        time.sleep(10)
        print("==========================")
        exam_angin_box = driver.find_element(By.CLASS_NAME, "but3")
        exam_angin = exam_angin_box.find_elements(By.TAG_NAME, "button")[1]
        exam_angin.click()
        swithExamCoursePage(driver)
    except Exception as e:
        print(e)
        print('\n', '>>>' * 20)
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
