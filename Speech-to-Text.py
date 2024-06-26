from google.cloud import speech, storage # Google Speech-To-Text
from pydub import AudioSegment  # 오디오 파일 채널 변경 하기 위해 사용
import tkinter as tk            # 팝업창 사용
from tkinter import filedialog
import os
from moviepy.editor import AudioFileClip    # 동영상에서 오디오 추출하기 위해 사용

dir_path = str(os.getcwd())
cur_file_path = str(os.path.dirname(os.path.realpath(__file__)))
dir_path = cur_file_path.replace(dir_path+'\\', '')

"""=====================================================
    음성 파일을 모노 오디오로 변환 
    // 매개변수 : 영상에서 추출한 음성 파일 경로 // 
-----------------------------------------------------"""
def convert_audio_to_mono(audio_file_path):
    global dir_path, cur_file_path
    
    file_name = str(audio_file_path).replace(dir_path + '/audio/','').replace('.wav','')
    print('file_name : ' + file_name)
    
    directory_mono = dir_path + '/audio/mono'
    if not os.path.exists(directory_mono):  # 폴더가 존재하지 않으면
        os.makedirs(directory_mono)  # 폴더를 생성합니다.

    # Check if audio file is mono. If not, convert it to mono.
    sound = AudioSegment.from_wav(audio_file_path)
    if sound.channels != 1:
        print("Converting stereo audio to mono.")
        sound = sound.set_channels(1)
        audio_file_path = directory_mono + '/' + "mono_" + file_name
        sound.export(audio_file_path, format="wav")
    
    upload_blob_from_memory('capstone_test1', audio_file_path, 'audio-files/'+file_name+'.wav', file_name)


"""==================================================
    구글 클라우드 버킷에 파일 업로드
    // 매개변수 : 버킷 이름, 모노 오디오 경로(로컬), 버킷에 저장될 경로, 전달할 파일 이름 // 
--------------------------------------------------"""
def upload_blob_from_memory(bucket_name, audio_file_path, destination_blob_name, file_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open(audio_file_path, "rb") as audio_file:
        blob.upload_from_file(audio_file)

    print(
        f"{destination_blob_name} with contents {audio_file_path} uploaded to {bucket_name}."
    )
    
    bucket_file_name = f"gs://{bucket_name}/{destination_blob_name}"
    transcribe_gcs_with_word_time_offsets(bucket_file_name, file_name)


"""=====================================================
    음성 파일을 srt 자막으로 변환 
    // 매개변수 : 음성 파일명, 전달 받은 파일명 // 
-----------------------------------------------------"""
def transcribe_gcs_with_word_time_offsets(gcs_uri: str, file_name: str):
    """Transcribe the given audio file asynchronously and output the word time offsets."""
    client = speech.SpeechClient()

    global dir_path
    directory = f"{dir_path}/result/srt/{file_name}"
    if not os.path.exists(directory):  # 폴더가 존재하지 않으면
        os.makedirs(directory)  # 폴더를 생성합니다.
    
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,  # 입력한 오디오 형식에 따라 달라짐 현재는 wav, 44100
        language_code="ko-KR",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=300)

    srt_file = f"{directory}/{file_name}_srt.srt"
    with open(srt_file, 'w') as f:
        index = 1
        for result in response.results:
            alternative = result.alternatives[0]

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.total_seconds()
                end_time = word_info.end_time.total_seconds()

                # Convert start and end times to srt format
                start_srt_format = f"{int(start_time // 3600):02d}:{int((start_time // 60) % 60):02d}:{int(start_time % 60):02d},{int((start_time % 1) * 1000):03d}"
                end_srt_format = f"{int(end_time // 3600):02d}:{int((end_time // 60) % 60):02d}:{int(end_time % 60):02d},{int((end_time % 1) * 1000):03d}"

                f.write(f"{index}\n")
                f.write(f"{start_srt_format} --> {end_srt_format}\n")
                f.write(f"{word}\n\n")

                index += 1

    return response

"""==================================================
    팝업창 띄워서 파일 선택 
    1. 영상 파일 선택하면 자동으로 음성 추출 (선택한 파일 이름이 팝업 창에 뜰 때까지 기다리기ㅣ)
    2. 확인 누르면 모노 오디오로 변환 -> srt 자막 생성 (오래걸림)
--------------------------------------------------"""
wav_filename_copy = ""

def open_file_dialog():
    global wav_filename_copy
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    file_label.config(text=file_name)

    global dir_path, cur_file_path
    #print('최종 dir_path : '+dir_path)
    
    directory = dir_path+'/audio/'
    if not os.path.exists(directory):  # 폴더가 존재하지 않으면
        os.makedirs(directory)  # 폴더를 생성합니다.
        
    # 파일 확장자 확인
    file_extension = os.path.splitext(file_name)[1]
    # MP4 동영상에서 오디오 추출
    if file_extension.lower() != '.wav':
        audioclip = AudioFileClip(file_path)
        wav_filename = os.path.splitext(file_name)[0] + '.wav'
        wav_filename = directory + wav_filename
        #print('wav_filename : '+wav_filename)
        audioclip.write_audiofile(wav_filename)  # WAV 파일로 저장
    else:
        wav_filename = file_name
    wav_filename_copy = wav_filename

def confirm():
    global wav_filename_copy
    print("선택한 파일 : " + file_label.cget("text") + "\n변환된 음성 파일 경로 : " + wav_filename_copy)
    convert_audio_to_mono(wav_filename_copy) #file_label.cget("text")
    #transcribe_file(wav_filename_copy)
    root.quit()

root = tk.Tk()
root.title("발표 영상 또는 음성 파일을 선택하세요.")

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
"""=================================================="""