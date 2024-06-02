
import cv2
import Calculate_Angle as ca
import matplotlib.pyplot as plt


def classifyPose(landmarks, output_image, mp_pose,filename, instance, display=False):
    '''자세 분류 함수, 자동완성 코드'''
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
                   
    if((right_elbow_angle < 55 and right_elbow_angle > 9) and
        (left_elbow_angle < 180 and left_elbow_angle > 153) and 
        (right_shoulder_angle < 46 and right_shoulder_angle > 14) and
        (left_shoulder_angle < 23 and left_shoulder_angle > 6)) :
        label = 'Hand_Forward'

    if((right_elbow_angle < 358 and right_elbow_angle > 2) and
        (left_elbow_angle < 28 and left_elbow_angle > 6) and 
        (right_shoulder_angle < 37 and right_shoulder_angle > 16) and
        (left_shoulder_angle < 34 and left_shoulder_angle > 18)) :
        label = 'Hands_on_Chest'

    if((right_elbow_angle < 50 and right_elbow_angle > 5) and
        (left_elbow_angle < 358 and left_elbow_angle > 301) and 
        (right_shoulder_angle < 38 and right_shoulder_angle > 17) and
        (left_shoulder_angle < 37 and left_shoulder_angle > 19)) :
        label = 'Attention'
    
    if((right_elbow_angle < 235 and right_elbow_angle > 182) and
        (left_elbow_angle < 251 and left_elbow_angle > 210) and 
        (right_shoulder_angle < 25 and right_shoulder_angle > 12) and
        (left_shoulder_angle < 68 and left_shoulder_angle > 15)) :
        label = 'Pointing_Pose'


    idx = str(filename).replace('clip_','').replace('.mp4','')
    idx = int(idx.split('/')[-1])
    
    if label != 'Unknown Pose':
        color = (0, 255, 0)
        
        if label == instance.check_dict[idx]:  #등록된 라벨이랑 같은거
            #instance.result_dict[idx] = 1
            instance.temp_list.append(1)
            print('idx : '+str(idx)+', 인식된 포즈(label) : '+label+', 키워드의 포즈(check_dict) : '+instance.check_dict[idx])

        elif label != instance.check_dict[idx]:   #등록된 라벨이랑 다른거
            #instance.result_dict[idx] = 2
            instance.temp_list.append(2)
            print('idx : '+str(idx)+', 인식된 포즈(label) : '+label+', 키워드의 포즈(check_dict)'+instance.check_dict[idx])
    
    else:   #아예 unknown으로
            #instance.result_dict[idx] = 0
            instance.temp_list.append(0)
            print('idx : '+str(idx)+', 인식된 포즈(label) : '+label+', 키워드의 포즈(check_dict)'+instance.check_dict[idx])
    
   
    # cv2.putText(output_image, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    # cv2.putText(output_image, "left_knee_angle: "+str(left_knee_angle), (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    # cv2.putText(output_image, "right_knee_angle: "+str(right_knee_angle), (10, 90), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    # cv2.putText(output_image, "left_elbow_angle: "+str(left_elbow_angle), (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    # cv2.putText(output_image, "right_elbow_angle: "+str(right_elbow_angle), (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    # cv2.putText(output_image, "left_shoulder_angle: "+str(left_shoulder_angle), (10, 180), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    # cv2.putText(output_image, "right_shoulder_angle: "+str(right_shoulder_angle), (10, 210), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
   
    # if display:
        
    #     plt.figure(figsize=[640,640])
    #     plt.imshow(output_image[:,:,::-1])
    #     plt.title("Output Image")
    #     plt.axis('off');
    # else :
    #     return output_image, label
    
    
