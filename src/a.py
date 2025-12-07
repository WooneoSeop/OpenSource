import matplotlib.pyplot as plt
from PIL import Image

img = Image.open("1.png")

fig, ax =plt.subplots(figsize=(10,10))
ax.imshow(img)
ax.set_title("HBNU")
points = []

output_file = "polar_coordinate.txt"

def click(c):
    x,y = c.xdata, c.ydata
    print(f"({x:.2f},{y:.2f})")

    points.append((x,y))
    with open(output_file, "a") as f:
        f.write(f"({x:.2f},{y:.2f})\n")

    ax.plot(x,y,'ro')
    fig.canvas.draw()
    
cid = fig.canvas.mpl_connect('button_press_event', click)

plt.show()

