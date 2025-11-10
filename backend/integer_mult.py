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

def karatsuba_multiply(x, y):
    """divide-and-conquer multiplication algorithm"""
    # Base case: if numbers are small enough, use regular multiplication
    if x < 10 or y < 10:
        return x * y, [(x, y, x * y, "Base case")]
    
    # Calculate the size of the numbers
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    
    # Split the digit sequences in the middle
    high1, low1 = x // (10**m), x % (10**m)
    high2, low2 = y // (10**m), y % (10**m)
    
    # Recursive steps
    z0, steps0 = karatsuba_multiply(low1, low2)
    z1, steps1 = karatsuba_multiply((low1 + high1), (low2 + high2))
    z2, steps2 = karatsuba_multiply(high1, high2)
    
    # Combine the results
    result = z2 * (10**(2*m)) + (z1 - z2 - z0) * (10**m) + z0
    
    # Collect all steps for visualization
    all_steps = steps0 + steps1 + steps2
    all_steps.append((x, y, result, f"Combine: z2*10^{2*m} + (z1-z2-z0)*10^{m} + z0"))
    
    return result, all_steps

def multiply_with_steps(a, b):
    """Return final product and list of partial products using divide-and-conquer"""
    final, all_steps = karatsuba_multiply(a, b)
    
    # Filter to show only the main recursive calls (not base cases unless they're interesting)
    partials_info = []
    for step in all_steps:
        x, y, product, description = step
        # Only include steps where at least one number has more than 1 digit
        if description != "Base case" or (x >= 10 or y >= 10):
            partials_info.append({
                'x': x,
                'y': y, 
                'product': product,
                'description': description
            })
    
    return final, partials_info

def format_steps(a, b, final, partials):
    """Return string showing step-by-step multiplication using divide-and-conquer"""
    lines = [f"Multiplying {a} × {b} using Divide-and-Conquer:"]
    lines.append(f"Final Product: {final}")
    lines.append("")
    lines.append("Recursive Steps:")
    lines.append("-" * 50)
    
    for i, step in enumerate(partials):
        desc = step['description']
        if desc == "Base case":
            lines.append(f"Step {i+1}: {step['x']} × {step['y']} = {step['product']} (Base Case)")
        else:
            lines.append(f"Step {i+1}: {step['x']} × {step['y']} = {step['product']}")
            lines.append(f"       {desc}")
    
    lines.append("-" * 50)
    return "\n".join(lines)

def show_results_gui(results, elapsed):
    win = tk.Toplevel()
    win.title("Multiplication Steps - Divide & Conquer")
    win.geometry("700x600")

    scrollbar = tk.Scrollbar(win)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text = tk.Text(win, wrap=tk.NONE, yscrollcommand=scrollbar.set, font=("Courier", 10))
    text.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=text.yview)

    # Display all multiplication steps
    for a, b, final, partials in results:
        text.insert(tk.END, format_steps(a, b, final, partials) + "\n\n")

    text.insert(tk.END, f"\nTotal time: {elapsed:.6f}s\n")

    # --- Plotting with proper x-axis spacing ---
    labels = [f"{a}x{b}" for a, b, _, _ in results]
    products = [final for _, _, final, _ in results]
    num_bars = len(labels)

    fig_width = max(8, num_bars * 0.6)
    fig_height = 6
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

 
    x_pos = np.arange(num_bars)
    bar_width = 0.6 if num_bars <= 15 else max(0.3, 12/num_bars)

    bars = ax.bar(x_pos, products, width=bar_width, color='lightgreen',
                  edgecolor='darkgreen', alpha=0.7, linewidth=1)

    # X-axis labels 
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=90, ha='right', fontsize=8)
    ax.set_ylabel("Product (A*B)", fontsize=12, fontweight='bold')
    ax.set_title("Integer Multiplication Results (Divide & Conquer)", fontsize=14, fontweight='bold', pad=20)
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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Step-by-step Integer Multiplication using Divide & Conquer")
    parser.add_argument('--file1', help='first input file path', default=None)
    parser.add_argument('--file2', help='second input file path', default=None)
    parser.add_argument('--gui', action='store_true', help='open GUI')
    args = parser.parse_args()

    if args.gui:
        root = tk.Tk()
        root.title("Integer Multiplication - Divide & Conquer")
        root.geometry("450x120")

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

        btn = tk.Button(root, text="Choose two files and multiply (Divide & Conquer)", command=open_and_run)
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