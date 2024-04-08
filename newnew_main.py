import tkinter as tk            # 팝업창 사용
from tkinter import filedialog
import os
import sys
#from Speech_to_Txt.makeClip import confirm

def open_file_dialog():
    global file_label
    global confirm_button
    '''파일 선택 대화 상자를 열고 사용자가 선택한 파일의 경로를 전역 변수 file_path에 저장, 선택된 파일의 이름을 file_label 레이블에 표시'''
    
    global file_path  # 전역 변수 file_path 추가
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    file_label.config(text=file_name)
    file_label.place(relx=0.4, rely=0.75, anchor=tk.CENTER)
    confirm_button.place(relx=0.7, rely=0.75, anchor=tk.CENTER)

#====================제목================================
root = tk.Tk()
root.title("니니의 발표 연습")
root.geometry("400x450")
label_title=tk.Label(root, text="니니의 발표 연습",font=('Arial',30))
label_title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

#=================사용방법/동영상 선택 버튼====================
btn_tutorial=tk.Button(root, text="사용 방법", width=15)
btn_tutorial.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

btn_select=tk.Button(root, text="동영상 선택", width=15, command=open_file_dialog)
btn_select.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# 선택한 파일 이름을 표시할 레이블
file_label = tk.Label(root, text="", bg='white', width=15, height=2)  # 기본 크기를 길게 설정

# 확인 버튼
confirm_button = tk.Button(root, text="확인", width=5, height=2, relief="groove")

root.mainloop()
