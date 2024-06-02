def condition(df_result, label):
    '''csv 파일에 값을 가져와서 조건문을 txt로 생성'''
    # template_code = f"""
    # if((right_knee_angle < {df_result.loc[4, 'max']} and right_knee_angle > {df_result.loc[4, 'min']}) and
    #     (left_knee_angle < {df_result.loc[5, 'max']} and left_knee_angle > {df_result.loc[5, 'min']})) :
    #     label = '{label}'
    # """
    
    # '''상체 위주'''
    template_code = f"""
    if((right_elbow_angle < {df_result.loc[0, 'max']} and right_elbow_angle > {df_result.loc[0, 'min']}) and
        (left_elbow_angle < {df_result.loc[1, 'max']} and left_elbow_angle > {df_result.loc[1, 'min']}) and 
        (right_shoulder_angle < {df_result.loc[2, 'max']} and right_shoulder_angle > {df_result.loc[2, 'min']}) and
        (left_shoulder_angle < {df_result.loc[3, 'max']} and left_shoulder_angle > {df_result.loc[3, 'min']})) :
        label = '{label}'
    """

    with open(r'..\MediaPipe\PoseCondition.txt', 'a') as file:
        file.write(template_code)