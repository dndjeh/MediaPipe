import math

def calculateAngle(landmark1, landmark2, landmark3):
    '''각도계산 함수'''
    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return int(angle)

def calculatePoseDifference(pose1, pose2):
    """
    Calculate the difference between two poses.

    Args:
        pose1: List of landmarks for the first pose.
        pose2: List of landmarks for the second pose.

    Returns:
        difference: Numeric value representing the pose difference.
    """
    # Here, you can define how to calculate the difference between two poses.
    # One simple way is to calculate the Euclidean distance between corresponding landmarks.
    # You may customize this part based on your requirements.

    # Example: Calculate the average Euclidean distance between corresponding landmarks.
    num_landmarks = len(pose1)
    total_distance = 0

    for i in range(num_landmarks):
        x1, y1, z1 = pose1[i]
        x2, y2, z2 = pose2[i]

        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        total_distance += distance

    average_distance = total_distance / num_landmarks

    return average_distance