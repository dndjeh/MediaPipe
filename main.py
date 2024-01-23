import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
import Classify_Pose as cp

import cv2
from cvzone.HandTrackingModule import HandDetector

# Initializing mediapipe pose class
# mediapipe pose class를 초기화 한다.
mp_pose = mp.solutions.pose

# Setting up the Pose function.
# pose detect function에 image detect=True, 최소감지신뢰도 = 0.3, 모델 복잡도 =2를 준다.
#pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
# mediapipe의 drawing class를 초기화한다.
mp_drawing = mp.solutions.drawing_utils

pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def detectPose(image, pose, display=True):
    '''이미지 인식 함수'''
    '''
    This function performs pose detection on an image.
    Args:
        image: The input image with a prominent person whose pose landmarks needs to be detected.
        pose: The pose setup function required to perform the pose detection.
        display: A boolean value that is if set to true the function displays the original input image, the resultant image, 
                 and the pose landmarks in 3D plot and returns nothing.
    Returns:
        output_image: The input image with the detected pose landmarks drawn.
        landmarks: A list of detected landmarks converted into their original scale.
    '''
    # 예시이미지 copy하기
    output_image = image.copy()

    # 컬러 이미지 BGR TO RGB 변환
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # pose detection 수행
    results = pose.process(imageRGB)

    # input image의 너비&높이 탐색
    height, width, _ = image.shape

    # detection landmarks를 저장할 빈 list 초기화
    landmarks = []
    
    # landmark가 감지 되었는지 확인
    if results.pose_landmarks:

      # landmark 그리기
      mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)

      # 감지된 landmark 반복
      for landmark in results.pose_landmarks.landmark:

        # landmark를 list에 추가하기
        landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))

    # 오리지널 image와 pose detect된 image 비교
    if display:

      # 오리지널 & 아웃풋 이미지 그리기
      plt.figure(figsize=[22,22])
      plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
      plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');

      # 3D 랜드마크 나타내기
      mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    # 그렇지 않다면, output_image 와 landmark return한다
    else:

      return output_image, landmarks
# pose detection function start

'''실시간 웹캠 포즈 인식'''
# Initialize the VideoCapture object to read from the webcam.
camera_video = cv2.VideoCapture(0)

# Initialize a resizable window.
cv2.namedWindow('Pose Classification', cv2.WINDOW_NORMAL)

w = camera_video.get(cv2.CAP_PROP_FRAME_WIDTH)
h = camera_video.get(cv2.CAP_PROP_FRAME_HEIGHT)


# 동영상 크기 변환
# camera_video.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 가로
# camera_video.set(cv2.CAP_PROP_FRAME_HEIGHT, 640) # 세로

# 변환된 동영상 크기 정보
w = camera_video.get(cv2.CAP_PROP_FRAME_WIDTH)
h = camera_video.get(cv2.CAP_PROP_FRAME_HEIGHT)


# Iterate until the webcam is accessed successfully.
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,) as hands:
    while camera_video.isOpened():
        
        # Read a frame.
        ok, frame = camera_video.read()

        # Check if frame is not read properly.
        if not ok:
            
            # Continue to the next iteration to read the next frame and ignore the empty camera frame.
            continue
        
        # Flip the frame horizontally for natural (selfie-view) visualization.
        frame = cv2.flip(frame, 1)
        
        # Get the width and height of the frame
        frame_height, frame_width, _ =  frame.shape
        
        # Resize the frame while keeping the aspect ratio.
        frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
        #frame = cv2.resize(frame, (1280, 1280))
        # Perform Pose landmark detection.
        frame, landmarks = detectPose(frame, pose_video, display=False)

        #---------------------------------------------------
        frame.flags.writeable = False
        results = hands.process(frame)

        # 이미지에 손 주석을 그립니다.
        frame.flags.writeable = True
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        #---------------------------------------------------
        # Check if the landmarks are detected.
        if landmarks:
            
            # Perform the Pose Classification.
            frame, _ = cp.classifyPose(landmarks, frame, mp_pose, display=False)
        
        # Display the frame.
        cv2.imshow('Pose Classification', frame)
        
        frame_height, frame_width, _ =  frame.shape

        # Wait until a key is pressed.
        # Retreive the ASCII code of the key pressed
        k = cv2.waitKey(1) & 0xFF
        
        # Check if 'ESC' is pressed.
        if(k == 27):
            
            # Break the loop.
            break

# Release the VideoCapture object and close the windows.
print(frame.shape)
camera_video.release()
cv2.destroyAllWindows()