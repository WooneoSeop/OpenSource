import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_file = os.path.join(BASE_DIR, "polar_coordinate.txt")
img_path = os.path.join(BASE_DIR, "1.png")

try:
    img = Image.open(img_path)
except FileNotFoundError:
    print(f"이미지 '{img_path}'을 찾을 수 없습니다.")
    exit()


fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(img)
ax.set_title("Draw: L-Click(Point), R-Click(Save), Wheel(Base Station)")

current_points = []
buildings = [] 
base_station = None
bs_plot = None


if os.path.exists(output_file):
    with open(output_file, "r") as f:
        temp_points = []
        for line in f:
            line = line.strip()
            if not line:
                if temp_points:
                    buildings.append(temp_points)
                    px, py = zip(*temp_points)
                    ax.plot(px, py, 'r-', linewidth=2, alpha=0.5)
                    temp_points = []
                continue
            parts = line.replace("(","").replace(")","").split(",")
            temp_points.append((float(parts[0]), float(parts[1])))


def click(event):
    global base_station, bs_plot, current_points

    if not event.xdata or not event.ydata: 
        return
    
    x, y = event.xdata, event.ydata

    
    if event.button == 1:
        current_points.append((x, y))
        ax.plot(x, y, 'ro', markersize=4)
        fig.canvas.draw()

    
    elif event.button == 3:
        if len(current_points) >= 2:
            closed_points = current_points + [current_points[0]]
            buildings.append(closed_points)
            with open(output_file, "a") as f:
                for px, py in closed_points:
                    f.write(f"({px:.2f},{py:.2f})\n")
                f.write("\n")
            
            px, py = zip(*closed_points)
            ax.plot(px, py, 'r-', linewidth=2)
            fig.canvas.draw()
            current_points.clear()

    
    elif event.button == 2:
        if bs_plot is not None:
            try:
                line = bs_plot.pop(0)
                line.remove()
            except Exception:
                pass 
        
        base_station = (x, y)
        bs_plot = ax.plot(x, y, 'gs', markersize=15, zorder=5)
        print(f"기지국 위치 갱신: ({x:.2f}, {y:.2f})")
        fig.canvas.draw()


fig.canvas.mpl_connect('button_press_event', click)
plt.show()