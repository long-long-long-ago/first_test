import json


def saveAnswer_w(quesrtion_dir):
    # "a" - 追加 - 会追加到文件的末尾
    # "w" - 写入 - 会覆盖任何已有的内容
    with open('ques.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(quesrtion_dir,ensure_ascii=False, indent=2))
    pass

def saveAnswer_a(quesrtion_dir):
    # "a" - 追加 - 会追加到文件的末尾
    # "w" - 写入 - 会覆盖任何已有的内容
    with open('ques.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(quesrtion_dir,ensure_ascii=False, indent=2))
    pass
