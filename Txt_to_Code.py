before_code = """
import cv2
import Calculate_Angle as ca
import matplotlib.pyplot as plt

def classifyPose(landmarks, output_image, mp_pose, display=False):
    '''자세 분류 함수'''
    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)
    
    # Calculate the required angles.
    #----------------------------------------------------------------------------------------------------------------
    
    # Get the angle between the left shoulder, elbow and wrist points. 
    # 11번, 13번, 15번 landmark 
    # 오른쪽 어깨, 왼쪽 팔꿈치, 왼쪽 손목 landmark angle 값 계산 
    right_elbow_angle = ca.calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
    # 12번, 14번, 16번 landmark 
    # 왼쪽 어깨, 오른쪽 팔꿈치, 오른쪽 손목 landmark angle 값 계산 
    left_elbow_angle = ca.calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    
    # 13번, 15번, 23번 landmark 
    # 오른쪽 어깨, 왼쪽 팔꿈치, 왼쪽 엉덩이, landmark angle 값 계산 
    right_shoulder_angle = ca.calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # 12번, 14번, 24번 landmark 
    # 왼쪽 어깨, 오른쪽 팔꿈치, 오른쪽 엉덩이 landmark angle 값 계산  
    left_shoulder_angle = ca.calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # 23번, 25번, 27번 landmark 
    # 오른쪽 엉덩이, 왼쪽 무릎, 왼쪽 발목 landmark angle 값 계산 
    right_knee_angle = ca.calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # 24번, 26번, 28번 landmark 
    # 왼쪽 엉덩이, 오른쪽 무릎, 오른쪽 발목  landmark angle 값 계산 
    left_knee_angle = ca.calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
                   
    """

#PoseCondition.txt 파일을 읽어서 condition_code에 저장한다.
code_path = '..\MediaPipe\PoseCondition.txt'
with open(code_path, 'r') as file:
    condition_code = file.read()

after_code = """
    
    if label != 'Unknown Pose':
        color = (0, 255, 0)  
    
   
    cv2.putText(output_image, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    cv2.putText(output_image, "left_knee_angle: "+str(left_knee_angle), (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.putText(output_image, "right_knee_angle: "+str(right_knee_angle), (10, 90), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    cv2.putText(output_image, "left_elbow_angle: "+str(left_elbow_angle), (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.putText(output_image, "right_elbow_angle: "+str(right_elbow_angle), (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    cv2.putText(output_image, "left_shoulder_angle: "+str(left_shoulder_angle), (10, 180), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.putText(output_image, "right_shoulder_angle: "+str(right_shoulder_angle), (10, 210), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

   
    if display:
        
        plt.figure(figsize=[640,640])
        plt.imshow(output_image[:,:,::-1])
        plt.title("Output Image")
        plt.axis('off');
    else :
        return output_image, label
"""


def pose_detection(landmarks, output_image, mp_pose, display=False):
    full_code = before_code + condition_code + after_code   #모든 코드를 합친다.

    #위 full_code를 Classify_Pose.py파일로 만들어 준다.
    with open('Classify_Pose.py', 'w', encoding='utf-8') as py_file:
        py_file.write(full_code)
    
    #위에서 만든 Classify_Pose.py파일을 불러와서 main.py로 return 한다.
    from Classify_Pose import classifyPose
    return classifyPose(landmarks, output_image, mp_pose, display=False)