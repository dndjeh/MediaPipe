# 폴더 이름
# [pt_video] 폴더 : 발표 영상
# [audio] 폴더 : 발표 영상에서 추출한 wav 파일
# ㄴ[mono] 폴더 : 모노로 변환한  wav 파일
# [result] 폴더 : 사용할 산출물 저장
# ㄴ[srt] 폴더 : 만들어진 srt 저장 폴더
# ㄴ[clips] 폴더 : 키워드 부분 추출된 영상 저장

# --------------------------------------------------------------------------------------------
# 개인키 설정 방법
# https://hyeo-noo.tistory.com/184

# 0. label_write.py에서 label 값 먼저 바꿔주기

# --------------------------------------------------------------------------------------------
# 이미지 데이터 직접 수집 시
# 1. Direct_image_generate/input_image에 원하는 자세 이미지를 넣는다.
# 2. Direct_image_generate/Image_Automation.py 실행 -> PoseCondition.txt 조건문 추가
# 3. main을 실행한다. -> 추가 조건을 포함한 Classify_Pose.py가 생성이 된다.

# ---------------------------------------------------------------------------------------------
# 실시간 Webcam으로 데이터 수집
# 1. Webcam_generate/Webcam_generate.py 실행시 다 자동으로 되도록 구현함
# 2. image 파일에 해당 label 이미지 파일이 생기고 txt 코드도 자동으로 작성됨
# 3. main을 실행한다. -> 추가 조건을 포함한 Classify_Pose.py가 생성이 된다.
# 60 프레임 단위로 저장 되는데 프레임 단위 바꾸고 싶으면 Webcam_generate.py 47번째 라인 if frame_count % 60 == 0: 숫자(프레임 단위) 변경하면 됨
# !!!!주의 사항!!!! 프레임 단위로 찍힐 때 포즈 잘 못 잡으면 각도 이상하게 나오니까 조심하기.

# ----------------------------------------------------------------------------------------------
# 수집한 영상으로 제스처 조건문 추가하기
# 0. Speech_to_Txt\makeClip_Data.py 실행 후 영상 srt 선택
# 1. Direct_image_generate\input_image 에 제스처별로 폴더가 생성되고, 이미지가 저장됨
# 2. Direct_image_generate\Image_Automation.py 에 145라인 pose값을 생성하고 싶은 제스처 이름으로 바꾼 후 실행 시 PoseCondition.txt에 조건문이 추가 됨

