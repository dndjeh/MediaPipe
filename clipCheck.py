import detect_video as dv
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from Speech_to_Txt import importingTest as it
import loadVideo as lv

# 인스턴스 생성
dv2 = dv.main2()

def main(only_filename, instance, root, loading_popup):
    global instance_it
    instance_it = instance
    clipChecking(only_filename, root, loading_popup)
    
# 현재 코드 파일의 디렉터리 위치 가져오기
dir_path = str(os.getcwd())
cur_file_path = str(os.path.dirname(os.path.realpath(__file__)))
dir_path = cur_file_path.replace(dir_path+'\\', '')

def clipChecking(file_name, root, loading_popup):
    global dir_path
    clip_dir_path = f"{dir_path}/Speech_to_Txt/result/clips/{file_name}"
    
    # 해당 폴더에 있는 모든 파일을 순회합니다.
    for file_path in Path(clip_dir_path).iterdir():
        if file_path.suffix == '.mp4':
            # idx 번호 추출 ex) clip_148 -> idx : 148
            idx = os.path.basename(file_path)
            idx = str(idx).replace('clip_','').replace('.mp4','')
            idx = int(idx.split('\\')[-1])
            
            instance_it.init_temp_list()
            
            dv.main2.Detect_From_Video(str(file_path), instance_it)
            print(instance_it.temp_list)
            if 1 in instance_it.temp_list :
                instance_it.result_dict[idx] = 1

            elif 2 in instance_it.temp_list :
                instance_it.result_dict[idx] = 2
                
            else :
                instance_it.result_dict[idx] = 0
    
    print()
    print('result_dict')
    print('=>')      
    print(instance_it.result_dict)

    
    lv.main(file_name, instance_it, root, loading_popup)