import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
txt_file = os.path.join(BASE_DIR, "..", "polar_coordinate.txt")
img_file = os.path.join(BASE_DIR, "..", "1.png")


import paint

base_station = getattr(paint, "base_station", None)

if base_station is None:
    print("기지국 위치가 설정되지 않았습니다. (휠 클릭으로 기지국을 찍어주세요)")
    sys.exit(1)

import cal
buildings = cal.read_coordinates(txt_file)

if buildings:
    print(f"{len(buildings)}개의 건물을 확인했습니다. 시각화를 시작합니다.")
    cal.visualize(img_file, buildings, base_station)
else:
    print("좌표 데이터가 없습니다. 도형을 그린 후 우클릭으로 저장했는지 확인하세요.")