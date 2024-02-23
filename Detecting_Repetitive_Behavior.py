import cv2
import Calculate_Angle as ca

# 최근 N 프레임의 포즈를 저장하는 리스트
recent_poses = []

# 반복되는 포즈 저장하는 리스트
repeat_poses=[]

# 얼마나 반복되는지 저장하는 리스트
num_repeat_poses=[]

# N을 조절하여 비교할 최근 프레임의 수 결졍하기
N = 40
difference_point=198
difference_point2=50

def DetectingRePetitiveBehavior(landmarks): #프레임 N 단위로 반복되는 동작 감지
    len_recent_poses=len(recent_poses)
    # 저장된 최근 프레임에서 포즈 비교
    if len_recent_poses >= N*2 and len_recent_poses%N==0:
        
        # 최근 N 프레임 간의 차이를 계산
        for i in range(0, len_recent_poses-N*2): 
            n=0
            pose_difference = 0
            for j in range(len_recent_poses-N,len_recent_poses): #현재 프레임 - n ~ 현재 프레임 비교
                pose_difference += ca.calculatePoseDifference(recent_poses[i+n], recent_poses[j])
                n+=1
            # 차이의 평균을 계산
            average_difference = pose_difference / (N)

            # 평균 차이가 일정 값 이하라면 반복되는 동작으로 간주
            if average_difference < difference_point:  # 이 값은 임의로 설정
                # 반복이 감지된 포즈는 repeat_poses에 저장
                repeat_poses.append(landmarks)
                print("반복되는 동작 감지!", average_difference)
                print("전 프레임",i+n)
                print("후 프레임",j)
                break
    # 현재 프레임의 포즈를 저장
    recent_poses.append(landmarks)
    
    
def Find_RB():
    len_repeat_poses=len(repeat_poses)

    for i in range(0,len_repeat_poses-1):
        pose_difference = 0
        n=0
        for j in range(i+1, len_repeat_poses):
            pose_difference += ca.calculatePoseDifference(repeat_poses[i], repeat_poses[j])
            n+=1
            # 차이의 평균을 계산
            average_difference = pose_difference / (N)
            
            # 평균 차이가 일정 값 이하라면 반복되는 동작으로 간주
            if average_difference < difference_point2:  # 이 값은 임의로 설정
                num_repeat_poses[i]+=1
                print("반복되는 동작 감지!", average_difference)
                print("전 프레임",i+n)
                print("후 프레임",j)