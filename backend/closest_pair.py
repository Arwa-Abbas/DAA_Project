# closest_pair.py
import math
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

def read_points_from_file(path):
    pts = []
    with open(path) as f:
        first = f.readline().strip()
        # if first line is integer, treat as count
        try:
            n = int(first)
            for _ in range(n):
                line = f.readline().strip()
                if not line:
                    break
                x, y = map(float, line.split())
                pts.append((x, y))
        except:
            # first line wasn't integer: treat it as a point
            if first:
                x, y = map(float, first.split())
                pts.append((x, y))
            for line in f:
                if line.strip():
                    x, y = map(float, line.split())
                    pts.append((x, y))
    return pts

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

# Brute force for small n
def brute_force(points):
    min_d = float('inf')
    pair = (None, None)
    n = len(points)
    for i in range(n):
        for j in range(i+1, n):
            d = dist(points[i], points[j])
            if d < min_d:
                min_d = d
                pair = (points[i], points[j])
    return min_d, pair

# Main D&C recursive function
def closest_pair_rec(px, py):
    n = len(px)
    if n <= 3:
        return brute_force(px)
    mid = n // 2
    midx = px[mid][0]

    Qx = px[:mid]
    Rx = px[mid:]
    # maintain y-sorted lists for left/right
    Qy = []
    Ry = []
    left_set = set(Qx)
    for p in py:
        if p in left_set:
            Qy.append(p)
        else:
            Ry.append(p)

    dl, pair_l = closest_pair_rec(Qx, Qy)
    dr, pair_r = closest_pair_rec(Rx, Ry)
    if dl < dr:
        d = dl
        pair = pair_l
    else:
        d = dr
        pair = pair_r

    # Build strip: points within d of midx in y-sorted order
    strip = [p for p in py if abs(p[0] - midx) < d]
    # Check up to next 7 points
    strip_len = len(strip)
    for i in range(strip_len):
        j = i + 1
        while j < strip_len and (strip[j][1] - strip[i][1]) < d:
            curd = dist(strip[i], strip[j])
            if curd < d:
                d = curd
                pair = (strip[i], strip[j])
            j += 1
    return d, pair

def closest_pair(points):
    if len(points) < 2:
        return None
    px = sorted(points, key=lambda p: (p[0], p[1]))
    py = sorted(points, key=lambda p: (p[1], p[0]))
    return closest_pair_rec(px, py)

# CLI run
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Closest pair D&C")
    parser.add_argument('--file', help='input file path', default=None)
    parser.add_argument('--gui', action='store_true', help='open GUI')
    args = parser.parse_args()

    if args.gui:
        # Simple tkinter GUI
        root = tk.Tk()
        root.title("Closest Pair Demo")
        root.geometry("400x120")

        def open_and_run():
            path = filedialog.askopenfilename(title="Select input file",
                                              filetypes=[("Text files", "*.txt"), ("All files","*.*")])
            if not path:
                return
            pts = read_points_from_file(path)
            if len(pts) < 2:
                messagebox.showerror("Error", "Need at least 2 points")
                return
            start = time.perf_counter()
            d, pair = closest_pair(pts)
            elapsed = time.perf_counter() - start
            # Plot
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            plt.figure(figsize=(6,6))
            plt.scatter(xs, ys, s=10)
            # highlight closest pair
            p1, p2 = pair
            plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], s=40)
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], linewidth=2)
            plt.title(f"Closest distance: {d:.6f}, time: {elapsed:.6f}s")
            plt.show()

        btn = tk.Button(root, text="Choose input file and run", command=open_and_run)
        btn.pack(pady=20)
        root.mainloop()

    else:
        if args.file is None:
            print("Use --file <path> or --gui")
        else:
            pts = read_points_from_file(args.file)
            if len(pts) < 2:
                print("Need at least 2 points.")
            else:
                start = time.perf_counter()
                d, pair = closest_pair(pts)
                elapsed = time.perf_counter() - start
                print(f"Points: {len(pts)}")
                print("Closest pair:", pair)
                print(f"Distance: {d:.6f}")
                print(f"Time: {elapsed:.6f}s")
