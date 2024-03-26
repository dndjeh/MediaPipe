import tkinter as tk            # 팝업창 사용
from tkinter import filedialog
import os
import pysrt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import chardet
import importingTest as importingTest

def get_encoding(file):
    '''주어진 파일의 인코딩 타입을 감지하고 반환, 자막 파일을 올바르게 읽기 위해 필요'''
    
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def open_file_dialog():
    '''파일 선택 대화 상자를 열고 사용자가 선택한 파일의 경로를 전역 변수 file_path에 저장, 선택된 파일의 이름을 file_label 레이블에 표시'''
    
    global file_path  # 전역 변수 file_path 추가
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    file_label.config(text=file_name)
    #print('file name : ' + file_name)
    #print('file_labe : ' + str(file_label.cget("text")))

def confirm():
    '''사용자가 선택한 자막 파일을 처리'''
    
    dir_path = str(os.getcwd())
    cur_file_path = str(os.path.dirname(os.path.realpath(__file__)))
    dir_path = cur_file_path.replace(dir_path+'\\', '')
    
    directory = dir_path + '/result/clips/' + str(file_label.cget("text")).replace('_srt.srt','')
    if not os.path.exists(directory):  # 폴더가 존재하지 않으면
        os.makedirs(directory)  # 폴더를 생성합니다.
        
    print("선택한 파일 : " + file_label.cget("text"))
    encoding = get_encoding(file_path)
    # srt 파일 로드
    subs = pysrt.open(file_path, encoding=encoding)
    
    # 1. 모든 자막의 텍스트를 저장
    sub_texts = []
    for sub in subs:
        sub_texts.append(sub.text)
    
    for test in sub_texts : print(test, sep=" ") # TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST 
    print()
    print("1번 자막 텍스트 저장 완료")
    
    # 2. 등록된 키워드가 저장된 리스트 불러오기
    pose_list = importingTest.pose_key
    keyword_dict = importingTest.keyword
    
    # 3. 리스트에 저장된 텍스트를 하나씩 등록된 키워드 리스트에 대조하며 일치하는지 비교
    check_list = []
    index = 0
    for sub in sub_texts:
        for key in pose_list:
            for keyword in keyword_dict[key]:
                # 4. 일치한다면 자막 인덱스와 일치한 키워드의 포즈 이름(키 값)을 저장
                if(sub == keyword):
                    check_list.append(index)
                    check_list.append(key)
        index += 1
    for test in check_list : print(test, sep=" ") # TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST  TEST 
    print()
    print("3번 비교 완료")
    
    # 5. 비교가 끝나면 체크 리스트에 있는 인덱스의 자막에 해당하는 타임라인 불러와서 영상 추출
    check_dict = {}
    index = 0
    for idx, key in zip(check_list[::2], check_list[1::2]): 
        check_dict[idx] = key
        
        sub = subs[idx]

        # 자막의 시작 시간과 끝 시간을 초 단위로 변환
        start_time = sub.start.ordinal / 1000  # 1000으로 나누는 이유는 ordinal이 밀리초 단위이기 때문
        end_time = sub.end.ordinal / 1000
        compensate = 0

        # 해당 시간대의 영상 잘라내기
        edited_filename = dir_path + '/pt_video/' + os.path.splitext(file_label.cget("text"))[0].replace('_srt', '')
        #print('edited_filename : ' + edited_filename)
        clip_path = directory + '/' + 'clip_' + str(idx) + '.mp4'
        #print('directory : ' + directory)
        #print('clip_path : ' + clip_path)
        ffmpeg_extract_subclip(edited_filename + '.mp4', start_time-compensate, end_time+compensate, targetname=clip_path)  # 추출 영상 이름을 'output_자막인덱스' 하면 나중에 영상 이름만 가지고(output_빼버리고 자막인덱스로) 영상의 원래 시간대 가져오는 거(sub(idx))랑 자막인덱스를 check_dict에 넣어서 키 이름도 가져올 수 있게 하는게 좋을듯
        index += 1
        
    root.quit()
    
'''
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
'''

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