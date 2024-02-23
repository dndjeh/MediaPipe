import os
import glob

def delete_latest_files(folder_path, num_files=3):
    try:
        # 해당 폴더 내의 모든 파일과 디렉토리 목록을 얻습니다.
        files = glob.glob(os.path.join(folder_path, '*'))

        # 파일 목록을 수정 시간에 따라 정렬합니다.
        sorted_files = sorted(files, key=os.path.getmtime, reverse=True)

        # 가장 최신 파일 num_files개를 삭제합니다.
        for i in range(min(num_files, len(sorted_files))):
            latest_file = sorted_files[i]
            os.remove(latest_file)
            print(f"Deleted the latest file: {latest_file}")

        if len(sorted_files) < num_files:
            print(f"Only {len(sorted_files)} file(s) found in the folder. All deleted.")

    except Exception as e:
        print(f"Error: {e}")