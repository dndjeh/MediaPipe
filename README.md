# 개인키 설정 방법
# https://hyeo-noo.tistory.com/184
# 0. input_image에 원하는 자세 이미지를 넣는다.
# 1. Pose_Condition_Txt.py 에서 label을 바꿔준다.(새로운 pose label 설정)
# 2. Image_Automation.py 을 실행한다.(스켈레톤을 추출해서 새로운 조건문을 txt로 작성 해줌)
# 3. main을 실행한다. -> 자동으로 새로 만든 조건문을 포함한 Classify_Pose.py가 생성이 된다.