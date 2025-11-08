import time
import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

def read_numbers_from_file(path):
    nums = []
    with open(path) as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if line:
                try:
                    num = int(line)
                    nums.append(num)
                except ValueError:
                    print(f"Skipping non-integer line {i}: {line}")
    return nums

def multiply_with_steps(a, b):
    """Return final product and list of partial products (like manual multiplication)"""
    a_str, b_str = str(a), str(b)
    partials = []
    b_rev = b_str[::-1]

    for i, digit in enumerate(b_rev):
        partial = int(digit) * a * (10**i)
        partials.append(partial)
    final = sum(partials)
    return final, partials

def format_steps(a, b, final, partials):
    """Return string showing step-by-step multiplication"""
    lines = [f"Multiplying {a} x {b}:"]

    b_str = str(b)
    for i, p in enumerate(partials):
        lines.append(f"{a} x {b_str[-(i+1)]} (shift {i}) = {p}")

    lines.append(f"Final Product: {final}")
    lines.append("-" * 30)
    return "\n".join(lines)

def show_results_gui(results, elapsed):
    win = tk.Toplevel()
    win.title("Multiplication Steps")
    win.geometry("600x500")

    scrollbar = tk.Scrollbar(win)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text = tk.Text(win, wrap=tk.NONE, yscrollcommand=scrollbar.set)
    text.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=text.yview)

    # Display all multiplication steps
    for a, b, final, partials in results:
        text.insert(tk.END, format_steps(a, b, final, partials) + "\n")

    text.insert(tk.END, f"\nTotal time: {elapsed:.6f}s\n")

    # --- Plotting with proper x-axis spacing ---
    labels = [f"{a}x{b}" for a, b, _, _ in results]
    products = [final for _, _, final, _ in results]
    num_bars = len(labels)

    # Figure size dynamically
    fig_width = max(8, num_bars * 0.6)
    fig_height = 6
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Bar spacing
    x_pos = np.arange(num_bars)
    bar_width = 0.6 if num_bars <= 15 else max(0.3, 12/num_bars)

    bars = ax.bar(x_pos, products, width=bar_width, color='skyblue',
                  edgecolor='navy', alpha=0.7, linewidth=1)

    # X-axis labels properly spaced and rotated
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=90, ha='right', fontsize=2)  # smaller font
    ax.set_ylabel("Product (A*B)", fontsize=12, fontweight='bold')
    ax.set_title("Integer Multiplication Results", fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.15, linestyle='--', linewidth=0.5)

    # Add value labels if few bars
    if num_bars <= 15:
        y_max = max(products)
        for bar, product in zip(bars, products):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + y_max*0.01,
                    f'{product}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout(pad=2.0)
    plt.show()

def multiply_files(file1, file2):
    nums1 = read_numbers_from_file(file1)
    nums2 = read_numbers_from_file(file2)

    if len(nums1) != len(nums2):
        print("Warning: Files have different lengths. Multiplying up to the shortest file.")

    results = []
    start = time.perf_counter()
    for a, b in zip(nums1, nums2):
        final, partials = multiply_with_steps(a, b)
        results.append((a, b, final, partials))
    elapsed = time.perf_counter() - start
    return results, elapsed

# CLI + GUI main
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Step-by-step Integer Multiplication")
    parser.add_argument('--file1', help='first input file path', default=None)
    parser.add_argument('--file2', help='second input file path', default=None)
    parser.add_argument('--gui', action='store_true', help='open GUI')
    args = parser.parse_args()

    if args.gui:
        root = tk.Tk()
        root.title("Integer Multiplication")
        root.geometry("400x120")

        def open_and_run():
            path1 = filedialog.askopenfilename(title="Select first input file",
                                               filetypes=[("Text files", "*.txt"), ("All files","*.*")])
            if not path1:
                return
            path2 = filedialog.askopenfilename(title="Select second input file",
                                               filetypes=[("Text files", "*.txt"), ("All files","*.*")])
            if not path2:
                return
            results, elapsed = multiply_files(path1, path2)
            if not results:
                messagebox.showerror("Error", "No valid numbers to multiply")
                return
            show_results_gui(results, elapsed)

        btn = tk.Button(root, text="Choose two files and multiply", command=open_and_run)
        btn.pack(pady=30)
        root.mainloop()
    else:
        if not args.file1 or not args.file2:
            print("Use --file1 <path> --file2 <path> or --gui")
        else:
            results, elapsed = multiply_files(args.file1, args.file2)
            if not results:
                print("No valid numbers to multiply")
            else:
                for a, b, final, partials in results:
                    print(format_steps(a, b, final, partials))
                print(f"\nTotal time: {elapsed:.6f}s")
