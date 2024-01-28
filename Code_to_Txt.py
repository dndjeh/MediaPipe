def change(df_result):
    template_code = """
    if((right_elbow_angle < {Right_Elbow_Angle_MAX} and right_elbow_angle > {Right_Elbow_Angle_MIN}) and
        (left_elbow_angle < {Left_Elbow_Angle_MAX} and left_elbow_angle > {Left_Elbow_Angle_MIN}) and 
        (right_shoulder_angle < {Right_Shoulder_Angle_MAX} and right_shoulder_angle > {Right_Shoulder_Angle_MIN}) and
        (left_shoulder_angle < {Left_Shoulder_Angle_MAX} and left_shoulder_angle > {Left_Shoulder_Angle_MIN}) and
        (right_knee_angle < {Right_Knee_Angle_MAX} and right_knee_angle > {Right_Knee_Angle_MIN}) and
        (left_knee_angle < {Left_Knee_Angle_MAX} and left_knee_angle > {Left_Knee_Angle_MIN})) :
        label = 'zzz'
    """

    with open(r'C:\JaeHyeok\Capstone\MediaPipe\PoseCondition.txt', 'a') as file:
        template_code = template_code.format(
            Right_Elbow_Angle_MAX=df_result.loc[0, 'max'],
            Right_Elbow_Angle_MIN=df_result.loc[0, 'min'],
            Left_Elbow_Angle_MAX=df_result.loc[1, 'max'],
            Left_Elbow_Angle_MIN=df_result.loc[1, 'min'],
            Right_Shoulder_Angle_MAX=df_result.loc[2, 'max'],
            Right_Shoulder_Angle_MIN=df_result.loc[2, 'min'],
            Left_Shoulder_Angle_MAX=df_result.loc[3, 'max'],
            Left_Shoulder_Angle_MIN=df_result.loc[3, 'min'],
            Right_Knee_Angle_MAX=df_result.loc[4, 'max'],
            Right_Knee_Angle_MIN=df_result.loc[4, 'min'],
            Left_Knee_Angle_MAX=df_result.loc[5, 'max'],
            Left_Knee_Angle_MIN=df_result.loc[5, 'min']
        )
        file.write(template_code)


    # 최종 코드 출력 또는 사용
    print(template_code)