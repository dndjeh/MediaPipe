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