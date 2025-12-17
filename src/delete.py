import os
import sys


file_path = "polar_coordinate.txt"


try:
    with open(file_path, "w") as f:

        f.truncate(0)

    print(f"'{file_path}' 파일이 초기화되었습니다.")


    
except Exception as e:
    print(f"파일 초기화 중 오류 발생: {e}")
    sys.exit(1) 