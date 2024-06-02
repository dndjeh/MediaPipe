from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import openai

window = Tk()
window.title("Chat GPT와 함께하는 발표 스크립트 짜기")
window.geometry("600x800")
num = 0
# Initialize the global variables
user_question = ""
gpt_answer = ""
script_file_path = ""

openai.api_key = "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"

def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're the assistant who polishes the presentation script."},
            {"role": "user", "content": question}
        ],
    )
    gpt_answer = response['choices'][0]['message']['content'].strip()
    return gpt_answer

def background_question():
    global user_question
    user_question = "배경: "
    user_question += background_answer.get()
    user_question += "\n"
    print(user_question)

def script_question():
    global user_question
    global gpt_answer
    global label_gpt_answer
    global script_file_path

    user_question += "발표 스크립트: "
    script_file_path = filedialog.askopenfilename()
    if script_file_path:
        with open(script_file_path, 'r', encoding='utf-8') as file:
            user_question += file.read()
        user_question += "\n 이걸 토대로 덜 쓴 부분 주제랑 배경에 맞게 추가해주고, 문장을 다듬어 주는 등 발표 스크립트를 있어보이게 해줘"
        print(user_question)
        
        gpt_answer = ask_gpt(user_question)
        
        if 'label_gpt_answer' in globals():
            label_gpt_answer.config(text=gpt_answer)
        else:
            label_gpt_answer = ttk.Label(window, text=gpt_answer)
            label_gpt_answer.config(wraplength=550)
            label_gpt_answer.pack()

def save_answer():
    global gpt_answer
    global script_file_path
    global num
    num += 1

    # 현재 코드가 실행되는 경로 확인
    current_path = os.getcwd()
    print(f"Current Path: {current_path}")

    # "Script_Folder" 경로 설정
    script_answers_folder = os.path.join(current_path, "Script_Folder")
    print(f"Script Answers Folder Path: {script_answers_folder}")

    # "Script_Folder" 폴더가 존재하지 않으면 생성
    if not os.path.exists(script_answers_folder):
        os.makedirs(script_answers_folder)
        print(f"Folder created: {script_answers_folder}")
    else:
        print("Folder already exists")

    if script_file_path:
        # 스크립트 파일 이름으로 된 하위 폴더 경로 설정
        script_file_name = os.path.splitext(os.path.basename(script_file_path))[0]
        script_specific_folder = os.path.join(script_answers_folder, script_file_name)
        print(f"Script Specific Folder Path: {script_specific_folder}")

        # 스크립트 파일 이름으로 된 하위 폴더가 존재하지 않으면 생성
        if not os.path.exists(script_specific_folder):
            os.makedirs(script_specific_folder)
            print(f"Folder created: {script_specific_folder}")
        else:
            print("Folder already exists")

        # 파일 이름 생성 및 저장
        file_name = f"{script_file_name}_gpt_answer_{num}.txt"
        file_path = os.path.join(script_specific_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(gpt_answer)
        print(f"Saved answer to {file_path}")
    else:
        print("No script file selected.")

def re_question():
    global user_question
    global gpt_answer
    global label_gpt_answer
    
    gpt_answer = ask_gpt(user_question)
    label_gpt_answer.config(text=gpt_answer)
    label_gpt_answer.config(wraplength=550)

question1 = ttk.Label(window, text="도우미: 어떤 상황에 발표를 하나요?")
question1.pack()

background_answer = ttk.Entry(window)
background_answer.pack()

btn = Button(window, text="입력하기", width=15, command=background_question)
btn.pack()

question2 = ttk.Label(window, text="도우미: 스크립트를 선택해주세요")
question2.pack()

btn_question2_click = Button(window, text="스크립트 선택", width=15, command=script_question)
btn_question2_click.pack()

btn_save_answer = Button(window, text="답변 파일 저장", width=15, command=save_answer)
btn_save_answer.pack()

btn_requestion = Button(window, text="다시 답변", width=15, command=re_question)
btn_requestion.pack()

window.mainloop()
