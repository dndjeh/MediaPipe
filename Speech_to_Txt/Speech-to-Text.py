from google.cloud import speech # Google Speech-To-Text
from pydub import AudioSegment  # 오디오 파일 채널 변경 하기 위해 사용
import tkinter as tk            # 팝업창 사용
from tkinter import filedialog
import os
from moviepy.editor import AudioFileClip    # 동영상에서 오디오 추출하기 위해 사용

"""=====================================================
    음성 파일을 텍스트로 변환 
    // 매개변수 : 음성 파일명 // 
-----------------------------------------------------"""
def transcribe_file(speech_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    directory = 'result/' + speech_file
    if not os.path.exists(directory):  # 폴더가 존재하지 않으면
        os.makedirs(directory)  # 폴더를 생성합니다.

    # Check if audio file is mono. If not, convert it to mono.
    sound = AudioSegment.from_wav(speech_file)
    if sound.channels != 1:
        print("Converting stereo audio to mono.")
        sound = sound.set_channels(1)
        speech_file = directory + '/' + "mono_" + speech_file
        sound.export(speech_file, format="wav")

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ko-KR",
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    with open(speech_file + '_out.txt', 'w') as f:  # -- 텍스트 저장시 사용
        for result in response.results:
            f.write(f"Transcript: {result.alternatives[0].transcript}\n")

    return response

"""=====================================================
    음성 파일을 srt 자막으로 변환 
    // 매개변수 : 음성 파일명 // 
-----------------------------------------------------"""
def transcribe_gcs_with_word_time_offsets(speech_file: str, ) -> speech.RecognizeResponse:
    """Transcribe the given audio file asynchronously and output the word time offsets."""
    from google.cloud import speech

    client = speech.SpeechClient()

    directory = 'result/' + speech_file
    if not os.path.exists(directory):  # 폴더가 존재하지 않으면
        os.makedirs(directory)  # 폴더를 생성합니다.

    # Check if audio file is mono. If not, convert it to mono.
    sound = AudioSegment.from_wav(speech_file)
    if sound.channels != 1:
        print("Converting stereo audio to mono.")
        sound = sound.set_channels(1)
        speech_file = directory + '/' + "mono_" + speech_file
        sound.export(speech_file, format="wav")


    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,    # 입력한 오디오 형식에 따라 달라짐 현재는 wav, 44100
        language_code="ko-KR",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    with open(speech_file + '_out.srt', 'w') as f:
        index = 1
        for result in result.results:
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

    return result

"""==================================================
팝업창 띄워서 파일 선택 
--------------------------------------------------"""
wav_filename_copy = ""

def open_file_dialog():
    global wav_filename_copy
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    file_label.config(text=file_name)

    # 파일 확장자 확인
    file_extension = os.path.splitext(file_name)[1]
    # MP4 동영상에서 오디오 추출
    if file_extension.lower() != '.wav':
        audioclip = AudioFileClip(file_path)
        wav_filename = os.path.splitext(file_name)[0] + '.wav'
        audioclip.write_audiofile(wav_filename)  # WAV 파일로 저장
    else:
        wav_filename = file_name
    wav_filename_copy = wav_filename

def confirm():
    global wav_filename_copy
    print("선택한 파일 : " + file_label.cget("text") + "\n변환된 음성 파일 : " + wav_filename_copy)
    transcribe_gcs_with_word_time_offsets(wav_filename_copy) #file_label.cget("text")
    transcribe_file(wav_filename_copy)
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
