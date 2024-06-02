import tkinter as tk
import os
from tkinter import messagebox
from tkvideo import tkvideo  # pip install tkvideo

dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, 'output')

def main(srt_timelist, srt_dict, file_name, real_root):
    # root = tk.Tk()
    root=tk.Toplevel(real_root)
    root.title("제스처 분석 결과")

    txt = tk.StringVar()
    txt.set('선택된 시각 : ')

    def open_file(i):
        selected_time = srt_timelist[i]
        idx = srt_dict[selected_time]
        video_path = os.path.join(output_path, file_name, f'{file_name}_{idx}.mp4')

        if os.path.exists(video_path):
            txt.set(f'선택된 시각 : {selected_time}')
            play_video(video_path)
        else:
            messagebox.showerror("Error", f"Video file {video_path} not found.")

    def play_video(video_path):
        for widget in video_frame.winfo_children():
            widget.destroy()
        video_label = tk.Label(video_frame)
        video_label.pack()
        try:
            player = tkvideo(video_path, video_label, loop=1, size=(1000, 600))
            player.play()
        except Exception as e:
            messagebox.showerror("Error", f"Could not play video: {e}")

    # 버튼들을 가로로 정렬하기 위해 Frame 사용
    button_frame = tk.Frame(root)
    button_frame.pack()
    if range(len(srt_timelist)==0):
        txt.set('제스처 사용을 잘 하시네요! 제스처가 추가로 필요한 부분이 인식되지 않았어요!')
    for i in range(len(srt_timelist)):
        btn = tk.Button(button_frame, text=srt_timelist[i], command=lambda i=i: open_file(i), width=10, height=2, relief="groove")
        btn.pack(side=tk.LEFT)  # 버튼들을 가로로 정렬

    # 레이블
    file_label = tk.Label(root, textvariable=txt, bg='white', height=2)
    file_label.pack()

    # 비디오 재생을 위한 프레임
    video_frame = tk.Frame(root)
    video_frame.pack()

    # root.mainloop()

# # 테스트 예시
# srt_timelist = ['00m 01s', '00m 22s']
# srt_dict = {'00m 01s': 24, '00m 22s': 25}
# file_name = 'test2'
# main(srt_timelist, srt_dict, file_name)