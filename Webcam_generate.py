import cv2
import time
import os
import Webcam_Automation  as WA
import label_write
#----------------------------------------- 자세 이름 작성하기
label = label_write.label
#-----------------------------------------

def capture_frames(label):
    '''웹캠 영상을 60프레임씩 자동으로 캡쳐한 후 저장'''
    # Open a connection to the webcam (0 is usually the default webcam)
    cap = cv2.VideoCapture(0)

    save_directory = f'{"../MediaPipe/Webcam_image/"+label}'
    print(save_directory)
    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # 비디오 저장
    # frame_width = int(cap.get(3))
    # frame_height = int(cap.get(4))
    # out = cv2.VideoWriter('captured_frames.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    os.makedirs(save_directory+"/input_"+label, exist_ok=True)
    os.makedirs(save_directory+"/output_"+label, exist_ok=True)
    # Capture frames continuously
    try:
        frame_count = 0
        while True:
            # Read a frame from the webcam
            ret, frame = cap.read()
            frame = cv2.flip(frame,1)
            # Check if the frame was read successfully
            if not ret:
                print("Error: Could not read frame.")
                break

            # Display the frame
            cv2.imshow('Webcam Feed', frame)

            # Save the frame as an image every 60 frames
            if frame_count % 60 == 0:
                image_name = f"captured_frame_{int(time.time())}.jpg"
                save_path = os.path.join(save_directory+"/input_"+label, image_name)
                cv2.imwrite(f'{save_path}', frame)
                print(f"Saved {save_path}")

            frame_count += 1

            # Exit the loop when the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Release the webcam and close the window
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_frames(label)
    WA.save(label)
