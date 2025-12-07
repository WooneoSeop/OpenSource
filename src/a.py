import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sys


output_file = "polar_coordinate.txt" 
img_path = "1.png"

try:
    img = Image.open(img_path)
except FileNotFoundError:
    print(f"오류: '{img_path}' 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
    sys.exit()


try:
    with open(output_file, "w") as f:
        f.write("")
    print(f"'{output_file}' 파일이 초기화되었습니다.")
except Exception as e:
    print(f"파일 초기화 중 오류 발생: {e}")
    sys.exit()


fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(img)
ax.set_title("Draw Shapes (L-Click: Point, R-Click: Finish Shape, X: Save & Show)")

current_points = []


def click(event):
    if not event.xdata or not event.ydata:
        return 

    x, y = event.xdata, event.ydata

    if event.button == 1: 
        print(f"좌표 추가: ({x:.2f}, {y:.2f})")
        
        ax.plot(x, y, 'ro')
        fig.canvas.draw()
    
        current_points.append((x, y))

    elif event.button == 3: 
        if len(current_points) >= 2:
            print("--- 도형 완성 ---")
            
            closed_points = current_points + [current_points[0]]
            
            with open(output_file, "a") as f:
                for px, py in closed_points:
                    f.write(f"({px:.2f},{py:.2f})\n")
                f.write("\n") 
                
            x_coords = [p[0] for p in closed_points]
            y_coords = [p[1] for p in closed_points]
            ax.plot(x_coords, y_coords, 'b-', linewidth=1.5, alpha=0.6)
            fig.canvas.draw()
            
            
            current_points.clear()
        else:
            print("경고: 도형을 완성하려면 최소 2개 이상의 좌표가 필요합니다.")
            

def on_close(event):
    print("\n창이 닫혔습니다. 최종 도형을 표시합니다.")
    
    
    final_read_points = []
    try:
        with open(output_file, "r") as f:
            current_shape = []
            for line in f:
                line = line.strip()
                if not line: 
                    if current_shape:
                        final_read_points.append(current_shape)
                        current_shape = []
                    continue
                
                
                try:
                    x_str, y_str = line.strip('()').split(',')
                    x = float(x_str)
                    y = float(y_str)
                    current_shape.append((x, y))
                except ValueError:
                    continue 
            
            if current_shape: 
                final_read_points.append(current_shape)

    except FileNotFoundError:
        print(f"오류: 좌표 파일 '{output_file}'을 찾을 수 없습니다.")
        return

    if not final_read_points:
        print("경고: 저장된 도형 좌표가 없습니다.")
        return

   
    fig_final, ax_final = plt.subplots(figsize=(10, 10))
    ax_final.imshow(img)
    ax_final.set_title("Final Drawn Shapes")
    

    FIXED_COLOR = 'b'
    
    
    
    for i, shape_points in enumerate(final_read_points):
        x_coords = [p[0] for p in shape_points]
        y_coords = [p[1] for p in shape_points]
        
     
        ax_final.plot(x_coords, y_coords, '-', 
                      color=FIXED_COLOR, linewidth=3, 
                      alpha=0.7, label=f"Shape {i+1}")
        
      
        ax_final.plot(x_coords[:-1], y_coords[:-1], 'o', 
                      color=FIXED_COLOR, markersize=6)
        
    ax_final.legend()
    plt.show()


cid_click = fig.canvas.mpl_connect('button_press_event', click)
cid_close = fig.canvas.mpl_connect('close_event', on_close)

plt.show()