import cv2
import os
from pathlib import Path
import chardet
import pysrt
from moviepy.editor import VideoFileClip, concatenate_videoclips
import makeOutputButtons as mob

dir_path = str(os.getcwd())
cur_file_path = str(os.path.dirname(os.path.realpath(__file__)))
dir_path = cur_file_path.replace(dir_path+'\\', '')

def get_encoding(file):
    '''주어진 파일의 인코딩 타입을 감지하고 반환, 자막 파일을 올바르게 읽기 위해 필요'''
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def main(file_name, instance, root, loading_popup):
    '''클립 영상과 클립의 키워드에서 취해야 할 제스처 영상을 병합한 영상 생성'''
    print("loadVideo")
    global instance_it, dir_path
    instance_it = instance
    srt_timelist = [] # 결과 버튼 구성에 사용될 시간 텍스트 리스트
    srt_dict = {} # 타임리스트로 srt 인덱스에 접근하기 위한 딕셔너리
    
    clip_dir_path = f"{dir_path}/Speech_to_Txt/result/clips/{file_name}"
    
    # 해당 폴더에 있는 모든 파일을 순회합니다.
    for file_path in Path(clip_dir_path).iterdir():
        if file_path.suffix == '.mp4':
            # idx 번호 추출 ex) clip_148 -> idx : 148
            idx = os.path.basename(file_path)
            idx = str(idx).replace('clip_','').replace('.mp4','')
            idx = int(idx.split('\\')[-1])
            
            if instance_it.result_dict[idx] == 0 or instance_it.result_dict[idx] == 2:
                pose_name = instance_it.check_dict[idx]
                main_video_path = str(file_path)
                overlay_video_path = f"{dir_path}/skeleton_video/{pose_name}.mp4"
                print('mv : '+main_video_path)
                print('ov :'+overlay_video_path)
                
                # srt 파일 로드, 해당 인덱스 키워드의 시작 시각 조회
                srt_path = f"{dir_path}/Speech_to_Txt/result/srt/{file_name}/{file_name}_srt.srt"
                encoding = get_encoding(srt_path)
                subs = pysrt.open(srt_path, encoding=encoding)
                start_time = subs[idx].start.ordinal / 1000
                srt_time = f"{int((start_time // 60) % 60):02d}m {int(start_time % 60):02d}s"
                # makeOutputButtons 파일로 넘기기 위한 정보 저장
                srt_timelist.append(srt_time)
                srt_dict[srt_time]=idx
                print('sub text : ', subs[idx].text)
                overlay_video(main_video_path, overlay_video_path, file_name, idx, srt_time, str(subs[idx].text))
    
    # 분석 결과 보고
    # srt_timelist, srt_dict, file_name 필요
    
    def close_loading_popup():
        loading_popup.destroy()
    
    root.after(0, close_loading_popup)
    print("letgo")
    mob.main(srt_timelist, srt_dict, file_name, root)
    
    # # 제스처 추천 영상들 병합 ============================================================
    # # 병합할 비디오 파일들이 들어 있는 폴더 경로
    # folder_path = f"{dir_path}/output/{file_name}/"

    # # 폴더 안의 모든 파일 리스트를 가져옴
    # files = os.listdir(folder_path)

    # # mp4 파일들만 걸러내기
    # video_files = [file for file in files if file.endswith(".mp4")]

    # # 비디오 클립들을 담을 리스트
    # video_clips = []

    # # 각 mp4 파일을 비디오 클립으로 변환하여 리스트에 추가
    # for video_file in video_files:
    #     video_clip = VideoFileClip(os.path.join(folder_path, video_file))
    #     video_clips.append(video_clip)

    # # 비디오 클립들을 연결하여 새로운 비디오 클립 생성
    # final_clip = concatenate_videoclips(video_clips)

    # # 결과를 저장할 파일명과 확장자 지정
    # final_clip.write_videofile("merged_video.mp4")

    # # 비디오 클립들을 해제
    # final_clip.close()
    # for clip in video_clips:
    #     clip.close()
    # # ============================================================
    
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def overlay_video(main_video_path, overlay_video_path, file_name, srt_idx, srt_time, sub_text):
    global dir_path
    cap_main = cv2.VideoCapture(main_video_path)
    cap_overlay = cv2.VideoCapture(overlay_video_path)
    
    if not cap_main.isOpened():
        print(f"Error opening main video file: {main_video_path}")
        return
    
    if not cap_overlay.isOpened():
        print(f"Error opening overlay video file: {overlay_video_path}")
        return

    # 저장할 비디오의 속성을 설정합니다.
    frame_width = int(cap_main.get(cv2.CAP_PROP_FRAME_WIDTH))  # 원본 동영상의 너비
    frame_height = int(cap_main.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 원본 동영상의 높이
    fps = cap_main.get(cv2.CAP_PROP_FPS)  # 원본 동영상의 FPS
    
    # VideoWriter 객체를 생성합니다. (*'mp4v'는 비디오 코덱을 의미. 필요에 따라 변경할 수 있다.)
    directory_output = f'{dir_path}/output/{file_name}' # output폴더 내에 파일명 폴더 생성
    if not os.path.exists(directory_output):  # 폴더가 존재하지 않으면
        os.makedirs(directory_output)  # 폴더를 생성합니다. 
    out = cv2.VideoWriter(f'{dir_path}/output/{file_name}/{file_name}_{srt_idx}.mp4', cv2.VideoWriter_fourcc(*'h264'), fps, (frame_width, frame_height))
    
    while True:
        ret_main, frame_main = cap_main.read()
        ret_overlay, frame_overlay = cap_overlay.read()
        
        if not ret_main:
            break
        
        # 프레임 오버레이 및 변환 코드 ===============================================================
        if not ret_overlay:
            cap_overlay.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 비교 동영상이 끝나면 처음으로 되돌립니다.
            ret_overlay, frame_overlay = cap_overlay.read()

        # 원본 동영상의 크기를 조정
        frame_main = cv2.resize(frame_main, (frame_width, frame_height))

        # 비교 동영상의 크기를 조절합니다.
        overlay_height = frame_main.shape[0] // 2
        overlay_width = frame_main.shape[1] // 4
        frame_overlay_resized = cv2.resize(frame_overlay, (overlay_width, overlay_height))

        # 오버레이 할 위치를 정의합니다.
        start_y = 0
        start_x = 0
        end_y = overlay_height
        end_x = overlay_width

        # 원본 동영상 위에 비교 동영상을 오버레이합니다.
        frame_main[start_y:end_y, start_x:end_x] = frame_overlay_resized

        # 한글 텍스트 추가========================================================
        pil_image = Image.fromarray(cv2.cvtColor(frame_main, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        try:
            # 한글 폰트 경로 설정 (시스템에 설치된 폰트 경로를 사용해야 함)
            font_path = f"{dir_path}\GmarketSansTTFLight.ttf"
            font_size = 40  # 원하는 폰트 크기로 변경
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # 하단 텍스트 추가
        # label = 'Point at ' + srt_time + ' in Video'
        # draw.rectangle([(0, frame_main.shape[0]-60), (600, frame_main.shape[0])], fill="white")
        # draw.text((0, frame_main.shape[0]-55), label, font=font, fill="black")
        
        # 상단 텍스트 추가
        label2 = '사용자 발언 키워드 : ' + sub_text
        draw.rectangle([(0, 0), (500, 60)], fill="white")
        draw.text((0, 5), label2, font=font, fill="black")
        
        # OpenCV 형식으로 변환
        frame_main = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        # 한글 텍스트 추가(끝)========================================================
        
        # 오버레이된 프레임을 저장합니다.
        out.write(frame_main)
        
        # 합쳐진 동영상을 보여줍니다.
        #cv2.imshow('Overlay Video', frame_main)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키를 누르면 종료합니다.
            break
    
    cap_main.release()
    cap_overlay.release()
    out.release()  # VideoWriter 객체를 해제합니다.
    cv2.destroyAllWindows()