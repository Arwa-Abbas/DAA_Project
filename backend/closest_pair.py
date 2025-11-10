import math
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
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
def brute_force(points, steps=None):
    min_d = float('inf')
    pair = (None, None)
    n = len(points)
    if steps is not None:
        steps.append(f"  Brute force on {n} points: {points}")
    
    for i in range(n):
        for j in range(i+1, n):
            d = dist(points[i], points[j])
            if d < min_d:
                min_d = d
                pair = (points[i], points[j])
                if steps is not None:
                    steps.append(f"    New min distance: {min_d:.4f} between {points[i]} and {points[j]}")
    
    if steps is not None:
        steps.append(f"  Brute force result: distance = {min_d:.4f}")
    return min_d, pair

# Main D&C recursive function with step tracking
def closest_pair_rec(px, py, depth=0, steps=None):
    indent = "  " * depth
    n = len(px)
    
    if steps is not None:
        steps.append(f"{indent}Level {depth}: Processing {n} points")
    
    # Base case
    if n <= 3:
        if steps is not None:
            steps.append(f"{indent}Base case reached (n <= 3), using brute force")
        return brute_force(px, steps)
    
    # DIVIDE PHASE
    mid = n // 2
    midx = px[mid][0]
    
    if steps is not None:
        steps.append(f"{indent}DIVIDE: Splitting at x = {midx:.2f}")
        steps.append(f"{indent}  Left half: {len(px[:mid])} points")
        steps.append(f"{indent}  Right half: {len(px[mid:])} points")
    
    Qx = px[:mid]
    Rx = px[mid:]
    
    # Maintain y-sorted lists for left/right
    Qy = []
    Ry = []
    left_set = set(Qx)
    for p in py:
        if p in left_set:
            Qy.append(p)
        else:
            Ry.append(p)
    
    # CONQUER PHASE (Recursive calls)
    if steps is not None:
        steps.append(f"{indent}CONQUER: Recursively solving left half")
    dl, pair_l = closest_pair_rec(Qx, Qy, depth + 1, steps)
    
    if steps is not None:
        steps.append(f"{indent}CONQUER: Recursively solving right half")
    dr, pair_r = closest_pair_rec(Rx, Ry, depth + 1, steps)
    
    # COMBINE PHASE
    if steps is not None:
        steps.append(f"{indent}COMBINE: Comparing results from left and right")
        steps.append(f"{indent}  Left min distance: {dl:.4f}")
        steps.append(f"{indent}  Right min distance: {dr:.4f}")
    
    if dl < dr:
        d = dl
        pair = pair_l
        if steps is not None:
            steps.append(f"{indent}  Taking left result (smaller distance)")
    else:
        d = dr
        pair = pair_r
        if steps is not None:
            steps.append(f"{indent}  Taking right result (smaller distance)")
    
    # Check strip around midline
    if steps is not None:
        steps.append(f"{indent}Checking strip around midline x = {midx:.2f} ± {d:.4f}")
    
    strip = [p for p in py if abs(p[0] - midx) < d]
    strip_len = len(strip)
    
    if steps is not None:
        steps.append(f"{indent}  Strip contains {strip_len} points")
    
    # Check combinations in strip
    strip_improved = False
    for i in range(strip_len):
        j = i + 1
        while j < strip_len and (strip[j][1] - strip[i][1]) < d:
            curd = dist(strip[i], strip[j])
            if curd < d:
                d = curd
                pair = (strip[i], strip[j])
                strip_improved = True
                if steps is not None:
                    steps.append(f"{indent}  🎯 New closest pair in strip: {strip[i]} and {strip[j]}")
                    steps.append(f"{indent}  New min distance: {d:.4f}")
            j += 1
    
    if steps is not None:
        if strip_improved:
            steps.append(f"{indent}✓ Strip check improved the result")
        else:
            steps.append(f"{indent}  Strip check didn't improve result")
        steps.append(f"{indent}Final result at level {depth}: distance = {d:.4f}")
    
    return d, pair

def closest_pair(points, steps=None):
    if len(points) < 2:
        return None, None
    
    if steps is not None:
        steps.append("Initial setup:")
        steps.append(f"  Total points: {len(points)}")
        steps.append("  Sorting points by x-coordinate...")
    
    px = sorted(points, key=lambda p: (p[0], p[1]))
    
    if steps is not None:
        steps.append("  Sorting points by y-coordinate...")
    
    py = sorted(points, key=lambda p: (p[1], p[0]))
    
    if steps is not None:
        steps.append("Starting divide-and-conquer algorithm...")
        steps.append("=" * 50)
    
    min_dist, pair = closest_pair_rec(px, py, 0, steps)
    
    if steps is not None:
        steps.append("=" * 50)
        steps.append(f"FINAL RESULT:")
        steps.append(f"  Closest pair: {pair[0]} and {pair[1]}")
        steps.append(f"  Minimum distance: {min_dist:.6f}")
    
    return min_dist, pair

def format_steps(steps):
    return "\n".join(steps)

# CLI run
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Closest pair D&C")
    parser.add_argument('--file', help='input file path', default=None)
    parser.add_argument('--gui', action='store_true', help='open GUI')
    parser.add_argument('--steps', action='store_true', help='show step-by-step process')
    args = parser.parse_args()

    if args.gui:
        # Enhanced tkinter GUI with steps
        root = tk.Tk()
        root.title("Closest Pair - Divide & Conquer")
        root.geometry("800x600")

        def open_and_run():
            path = filedialog.askopenfilename(title="Select input file",
                                              filetypes=[("Text files", "*.txt"), ("All files","*.*")])
            if not path:
                return
            pts = read_points_from_file(path)
            if len(pts) < 2:
                messagebox.showerror("Error", "Need at least 2 points")
                return
            
            # Create new window for results
            result_window = tk.Toplevel(root)
            result_window.title("Closest Pair Results")
            result_window.geometry("900x700")
            
            # Text area for steps
            text_frame = tk.Frame(result_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            text_area.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=text_area.yview)
            
            # Run algorithm
            steps = []
            start = time.perf_counter()
            d, pair = closest_pair(pts, steps)
            elapsed = time.perf_counter() - start
            
            # Display steps
            text_area.insert(tk.END, f"CLOSEST PAIR - DIVIDE AND CONQUER\n")
            text_area.insert(tk.END, f"Points: {len(pts)}\n")
            text_area.insert(tk.END, f"Time: {elapsed:.6f}s\n")
            text_area.insert(tk.END, "=" * 60 + "\n\n")
            
            for step in steps:
                text_area.insert(tk.END, step + "\n")
            
            text_area.config(state=tk.DISABLED)
            
            # Plot
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Plot 1: All points with closest pair highlighted
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax1.scatter(xs, ys, s=20, alpha=0.6, label="All points")
            
            # Highlight closest pair
            if pair:
                p1, p2 = pair
                ax1.scatter([p1[0], p2[0]], [p1[1], p2[1]], s=100, color='red', label='Closest pair')
                ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-', linewidth=2)
                
                # Add distance label
                mid_x = (p1[0] + p2[0]) / 2
                mid_y = (p1[1] + p2[1]) / 2
                ax1.text(mid_x, mid_y, f'd = {d:.4f}', fontsize=12, 
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
            
            ax1.set_xlabel('X')
            ax1.set_ylabel('Y')
            ax1.set_title(f'Closest Pair Visualization\nDistance: {d:.6f}')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Algorithm steps visualization
            ax2.axis('off')
            ax2.text(0.1, 0.9, 'Divide & Conquer Steps:', fontsize=14, fontweight='bold')
            ax2.text(0.1, 0.8, f'Total Points: {len(pts)}', fontsize=10)
            ax2.text(0.1, 0.7, f'Recursive Levels: {int(math.log2(len(pts)))}', fontsize=10)
            ax2.text(0.1, 0.6, f'Time Complexity: O(n log n)', fontsize=10)
            ax2.text(0.1, 0.5, f'Actual Time: {elapsed:.6f}s', fontsize=10)
            ax2.text(0.1, 0.4, f'Closest Distance: {d:.6f}', fontsize=10, color='red')
            
            if pair:
                ax2.text(0.1, 0.3, f'Pair: ({pair[0][0]:.2f}, {pair[0][1]:.2f})', fontsize=9)
                ax2.text(0.1, 0.25, f'      ({pair[1][0]:.2f}, {pair[1][1]:.2f})', fontsize=9)
            
            plt.tight_layout()
            plt.show()

        btn = tk.Button(root, text="Choose input file and run (Divide & Conquer)", 
                       command=open_and_run, bg='lightblue', font=('Arial', 12))
        btn.pack(pady=20)
        
        info_label = tk.Label(root, text="This implementation uses Divide & Conquer algorithm\nTime Complexity: O(n log n)", 
                             font=('Arial', 10), fg='darkgreen')
        info_label.pack(pady=10)
        
        root.mainloop()

    else:
        if args.file is None:
            print("Use --file <path> or --gui")
        else:
            pts = read_points_from_file(args.file)
            if len(pts) < 2:
                print("Need at least 2 points.")
            else:
                steps = [] if args.steps else None
                start = time.perf_counter()
                d, pair = closest_pair(pts, steps)
                elapsed = time.perf_counter() - start
                
                print(f"Points: {len(pts)}")
                print("Closest pair:", pair)
                print(f"Distance: {d:.6f}")
                print(f"Time: {elapsed:.6f}s")
                
                if args.steps and steps:
                    print("\n" + "="*60)
                    print("STEP-BY-STEP PROCESS:")
                    print("="*60)
                    for step in steps:
                        print(step)