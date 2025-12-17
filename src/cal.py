import math
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from shapely.geometry import LineString, Polygon, Point

def calculate_signal(x, y, base_station, buildings):
    bs_x, bs_y = base_station
    d = math.hypot(x - bs_x, y - bs_y)
    if d <= 1: return 100
    

    f=2400
    fs_loss = 20 * math.log10(d) + 20 * math.log10(f) - 147.55
    final_fs_loss = (fs_loss - 40) * 1.5

   
    path_line = LineString([(bs_x, bs_y), (x, y)])
    b_loss = 0
    for b in buildings:
        if len(b) >= 3:
            poly = Polygon(b)
            if path_line.intersects(poly):
                
                b_loss += 10 
                
    signal = 100 - (fs_loss + b_loss)
    return max(signal, 0)

def read_coordinates(file_path):
    buildings = []
    if not os.path.exists(file_path): return []
    with open(file_path, "r") as f:
        current_b = []
        for line in f:
            line = line.strip()
            if not line:
                if current_b: buildings.append(current_b); current_b = []
                continue
            parts = line.replace("(","").replace(")","").split(",")
            current_b.append((float(parts[0]), float(parts[1])))
    return buildings

def visualize(img_path, buildings, base_station):
    try:
        img = Image.open(img_path)
        img_w, img_h = img.size
    except:
        print("이미지 로드 실패"); return

   
    step = 20
    x_range = np.arange(0, img_w, step)
    y_range = np.arange(0, img_h, step)
    X, Y = np.meshgrid(x_range, y_range)
    
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = calculate_signal(X[i, j], Y[i, j], base_station, buildings)

    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(img, alpha=0.6)
    
    
    cp = ax.contourf(X, Y, Z, levels=30, cmap='RdYlGn', alpha=0.5)
    plt.colorbar(cp, label='Signal Strength')

   
    for b in buildings:
        poly_x, poly_y = zip(*b)
        ax.plot(poly_x, poly_y, 'k-', linewidth=2)

    if base_station:
        ax.plot(base_station[0], base_station[1], 'bs', markersize=15, label="Base Station")

    ax.set_title("Radio Signal Propagation Map")
    plt.legend()
    plt.show()