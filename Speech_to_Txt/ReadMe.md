# 코드 실행 전 환경 설정
***기본적으로 본인 구글 아이디가 Google Cloud 서비스 이용 권한이 있어야 한다.***

**1. gcloud SDK 설치**
   
    - 폴더 안에 있는 GoogleCloudSDKInstaller로 설치한다.

**2. 클라이언트 라이브러리 설치 (파이썬 내 google.cloud import speech 이 가능하도록 한다.)**
   
    - cmd에 아래 명령어 입력하여 설치
    
        pip install --upgrade google-cloud-speech

        pip install google-cloud-storage

**4. gcloud 초기 설정**

    - cmd에 아래 명령어 친다. 진행 중 구글 로그인 창 뜨면 로그인 하면 된다.

    gcloud init

**4. 3번 중에 Pick cloud project to use: 뜨면**

                 [2] Enter a project ID 선택 후 (프로젝트ID) 입력

**4. 구글 다시 로그인**

    - cmd에 아래 명령어 압력

    gcloud auth application-default login

**5. ADC 설정 문제 해결**

    - cmd에 아래 명령어 입력

    gcloud auth application-default set-quota-project (프로젝트ID)

**6. pydub, moviepy 같은 필요 파이썬 라이브러리는 알아서 설치 하면 된다.**

**7. 코드가 있는 경로상에 pt_video라는 폴더를 생성하고 해당 폴더에 발표 영상을 저장하고 코드를 사용해야 한다.**


# Speech-To-Text.py
**영상 파일을 넣으면 SRT 자막을 만들어주는 코드**

## 비디오 -> 오디오 -> 모노 오디오 -> 텍스트 + 타임라인 -> SRT 자막
### 1. convert_audio_to_mono(audio_file_path)
  
- 음성 파일을 모노 오디오로 변환하고 변환된 오디오 파일을 구글 클라우드 버킷에 업로드하는 함수 upload_blob_from_memory에 전달한다.

- 매개변수 : 영상에서 추출된 음성 파일의 경로

### 2. upload_blob_from_memory(bucket_name, audio_file_path, destination_blob_name, file_name)

- 구글 클라우드 버킷에 모노 오디오를 업로드하고 버킷 상의 모노 오디오의 경로를 텍스트와 타임라인을 추출하는 함수 transcribe_gcs_with_word_time_offsets에 전달한다.

- 매개변수 : 버킷 이름, 모노 오디오 경로(로컬), 버킷에 저장될 경로, 전달할 파일 이름

### 3. transcribe_gcs_with_word_time_offsets(gcs_uri: str, file_name: str)

- 구글 클라우드 버킷에 있는 모노 오디오에서 텍스트와 타임라인은 추출하고 이 정보를 조합해 SRT 자막을 생성한다.

- 매개변수 : 음성 파일명, 전달 받은 파일명

## 팝업창 띄워서 파일 선택
### 4. open_file_dialog()

- 파일 선택 팝업창을 띄워 파일을 선택하면 자동으로 비디오에서 음성을 추출하여 저장한다.

### 5. confirm()

- 팝업창의 확인 버튼이 눌렸을 때 실행되는 함수이다. 선택된 파일의 음성 파일 경로를 함수 convert_audio_to_mono에 전달한다.

### 함수의 실행 순서

- 4 : 영상 파일 선택 및 음성 추출
  
- 5 : 음성 파일을 다음 함수로 전달
  
- 1 : 음성을 모노 오디오로 변환
  
- 2 : 모노 오디오를 버킷에 저장
  
- 3 : 버킷에 저장된 오디오에서 텍스트와 타임라인을 추출하고 재조합 해 SRT 자막 생성


# makeClip.py

**만들어진 srt자막을 선택하면 importingTest.py에 기록되어 있는 자세 키워드와 자막 파일에 있는 키워드와 비교하여 일치하는 키워드에 대한 영상 클립을 원본 영상에서 추출하여 저장하는 코드**

1. 모든 자막의 텍스트를 저장

2. 등록된 키워드가 저장된 리스트 불러오기

3. 리스트에 저장된 텍스트를 하나씩 등록된 키워드 리스트에 대조하며 일치하는지 비교

4. 일치한다면 자막 인덱스와 일치한 키워드의 포즈 이름(키 값)을 저장

5. 비교가 끝나면 체크 리스트에 있는 인덱스의 자막에 해당하는 타임라인 불러와서 영상 추출
