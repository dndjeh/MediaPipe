import os
import cv2
import mediapipe as mp
import pandas as pd
from Webcam_Pose_Condition_Txt import condition
from Calculate_Angle import calculateAngle  # Assuming you have a Calculate_Angle module

mp_pose = mp.solutions.pose
def extract_skeleton(image_path):
    '''스켈레톤 추정하고, 각 관절의 각도를 이미지에 나타낸다'''
    
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
    
    # Read the image
    image = cv2.imread(image_path)
    target_size = (640, 853)
    image = cv2.resize(image, target_size)
    
    # Convert BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform pose detection
    results = pose.process(image_rgb)
    
    # Extract landmark coordinates
    landmarks = []
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((landmark.x, landmark.y, landmark.z if landmark.HasField('z') else 0))

        # Draw skeleton on the image
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        text_color = (0, 255, 0)

        right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

        left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   

        right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

        left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

        right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

        left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
        
        right_elbow_text = f"Right Elbow Angle: {right_elbow_angle:.2f} degrees"
        left_elbow_text = f"Left Elbow Angle: {left_elbow_angle:.2f} degrees"
        right_shoulder_text = f"Right Shoulder Angle: {right_shoulder_angle:.2f} degrees"
        left_shoulder_text = f"Left Shoulder Angle: {left_shoulder_angle:.2f} degrees"
        right_knee_text = f"Right Knee Angle: {right_knee_angle:.2f} degrees"
        left_knee_text = f"Left Knee Angle: {left_knee_angle:.2f} degrees"

        cv2.putText(image, right_elbow_text, (10, 30), font, font_scale, text_color, font_thickness)
        cv2.putText(image, left_elbow_text, (10, 60), font, font_scale, text_color, font_thickness)
        cv2.putText(image, right_shoulder_text, (10, 90), font, font_scale, text_color, font_thickness)
        cv2.putText(image, left_shoulder_text, (10, 120), font, font_scale, text_color, font_thickness)
        cv2.putText(image, right_knee_text, (10, 150), font, font_scale, text_color, font_thickness)
        cv2.putText(image, left_knee_text, (10, 180), font, font_scale, text_color, font_thickness)
    return landmarks, image, right_elbow_angle, left_elbow_angle, right_shoulder_angle, left_shoulder_angle, right_knee_angle, left_knee_angle


def process_images(folder_path, output_csv, output_image_folder, label):
    '''관절의 각도를 csv파일로 정리하고, condition 함수를 불러서 조건문을 PoseCondition.txt로 저장해준다.'''
    data = []
    
    os.makedirs(output_image_folder, exist_ok=True)

    all_right_elbow_angles = []
    all_left_elbow_angles = []
    all_right_shoulder_angles = []
    all_left_shoulder_angles = []
    all_right_knee_angles = []
    all_left_knee_angles = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)

            landmarks, annotated_image, right_elbow_angle, left_elbow_angle, right_shoulder_angle, left_shoulder_angle, right_knee_angle, left_knee_angle = extract_skeleton(image_path)

            data.append({'Image': filename,
                         'Right_Elbow_Angle': right_elbow_angle,
                         'Left_Elbow_Angle': left_elbow_angle,
                         'Right_Shoulder_Angle': right_shoulder_angle,
                         'Left_Shoulder_Angle': left_shoulder_angle,
                         'Right_Knee_Angle': right_knee_angle,
                         'Left_Knee_Angle': left_knee_angle})

            all_right_elbow_angles.append(right_elbow_angle)
            all_left_elbow_angles.append(left_elbow_angle)
            all_right_shoulder_angles.append(right_shoulder_angle)
            all_left_shoulder_angles.append(left_shoulder_angle)
            all_right_knee_angles.append(right_knee_angle)
            all_left_knee_angles.append(left_knee_angle)

            output_image_path = os.path.join(output_image_folder, f"annotated_{filename}")
            cv2.imwrite(output_image_path, annotated_image)


    df = pd.DataFrame(data)
    df_mean =pd.DataFrame({'mean':df.iloc[:,1:].mean()})
    df_max = pd.DataFrame({'max':df.iloc[:,1:].max()})
    df_min = pd.DataFrame({'min':df.iloc[:,1:].min()})
    df_result = pd.concat([df_mean,df_max,df_min],axis=1)
    df_result = df_result.reset_index()

    total_output_csv_path = '../MediaPipe/output_csv/total_result.csv'
    df.to_csv(output_csv, index=False)
    df_result.to_csv(total_output_csv_path, index=False)    #mean, max, min을 저장하는 csv파일 생성

    #저장된 csv 파일에 값을 가져와서 조건문을 txt로 생성
    condition(df_result)
def save(label):
    # 인풋 이미지 폴더 경로와 아웃 풋 이미지 폴더 경로 설정, 그리고 각 관절의 각도를 저장할 csv 파일 저장 경로
    image_folder_path = f'{"../MediaPipe/Webcam_image/"+label+"/input_"+label}'
    output_image_folder = f'{"../MediaPipe/Webcam_image/"+label+"/output_"+label}'
    output_csv_path = '../MediaPipe/output_csv/angle.csv'
    process_images(image_folder_path, output_csv_path, output_image_folder, label)
