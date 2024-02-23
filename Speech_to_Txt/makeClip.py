import tkinter as tk            # 팝업창 사용
from tkinter import filedialog
import os
import pysrt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import chardet

def get_encoding(file):
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def open_file_dialog():
    global file_path  # 전역 변수 file_path 추가
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    file_label.config(text=file_name)

def confirm():
    print("선택한 파일 : " + file_label.cget("text"))
    encoding = get_encoding(file_path)
    # srt 파일 로드
    subs = pysrt.open(file_path, encoding=encoding)

    # 원하는 인덱스의 자막 선택 (인덱스는 0부터 시작)
    idx = 13  # 원하는 인덱스로 변경
    sub = subs[idx]

    # 자막의 시작 시간과 끝 시간을 초 단위로 변환
    start_time = sub.start.ordinal / 1000  # 1000으로 나누는 이유는 ordinal이 밀리초 단위이기 때문
    end_time = sub.end.ordinal / 1000
    compensate = 1

    # 해당 시간대의 영상 잘라내기
    edited_filename = os.path.splitext(file_label.cget("text"))[0].replace('mono_', '').replace('.wav_out', '')
    print('edited_filename : ' + edited_filename)
    ffmpeg_extract_subclip(edited_filename + '.mp4', start_time-compensate, end_time+compensate, targetname="output.mp4")
    root.quit()

root = tk.Tk()
root.title("자막 파일을 선택하세요.")

# 파일 선택 버튼
file_button = tk.Button(root, text="파일 선택", command=open_file_dialog, width=10, height=2, relief="groove")
file_button.grid(row=0, column=0)  # grid를 사용하여 배치

# 선택한 파일 이름을 표시할 레이블
file_label = tk.Label(root, text="", bg='white', width=30, height=2)  # 기본 크기를 길게 설정
file_label.grid(row=0, column=1)  # grid를 사용하여 배치
file_label.grid_propagate(False)  # 크기 고정

# 확인 버튼
confirm_button = tk.Button(root, text="확인", command=confirm, width=10, height=2, relief="groove")
confirm_button.grid(row=0, column=2)  # grid를 사용하여 배치

root.mainloop()