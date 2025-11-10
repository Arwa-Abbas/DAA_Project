import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import math

st.set_page_config(page_title="DAA Project", layout="wide")

# CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(-45deg, #1a0b2e, #2d1b69, #1e3a8a, #3730a3);
        background-size: 400% 400%;
        animation: gradientFlow 20s ease infinite;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(96, 165, 250, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
        animation: particleFloat 15s ease infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particleFloat {
        0%, 100% { opacity: 0.3; transform: translateY(0px); }
        50% { opacity: 0.6; transform: translateY(-20px); }
    }
    
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-weight: 800 !important;
        font-size: 3rem !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #ec4899, #60a5fa);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: neonGlow 3s ease-in-out infinite, gradientShift 4s ease infinite;
        margin-bottom: 2rem !important;
    }
    
    @keyframes neonGlow {
        0%, 100% { 
            filter: drop-shadow(0 0 20px rgba(96, 165, 250, 0.8))
                    drop-shadow(0 0 40px rgba(167, 139, 250, 0.5));
        }
        50% { 
            filter: drop-shadow(0 0 30px rgba(167, 139, 250, 0.9))
                    drop-shadow(0 0 60px rgba(236, 72, 153, 0.6));
        }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    h2 {
        color: #e0e7ff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        padding: 1rem 1.5rem;
        background: rgba(59, 130, 246, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(96, 165, 250, 0.2);
        margin: 1.5rem 0 !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(30, 27, 75, 0.7) !important;
        backdrop-filter: blur(30px) saturate(180%);
        border-right: 2px solid rgba(139, 92, 246, 0.3);
    }
    
    .step-card {
        background: rgba(59, 130, 246, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 1rem;
        margin: 0.5rem 0;
        color: #e0e7ff;
        animation: slideInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(96, 165, 250, 0.3);
        border-color: rgba(167, 139, 250, 0.5);
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(167, 139, 250, 0.15));
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 2px solid rgba(96, 165, 250, 0.4);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Divide & Conquer Algorithms")

# Sidebar
algo_choice = st.sidebar.selectbox(
    "Select Algorithm",
    ["Closest Pair of Points", "Integer Multiplication"]
)

# Helper Functions
def distance(p1, p2):
    return math.dist(p1, p2)

def brute_force_closest(points, steps=None):
    """Brute force for small sets (base case)"""
    min_dist = float("inf")
    pair = (None, None)
    n = len(points)
    
    if steps is not None:
        steps.append(f"  Base case: Brute force on {n} points")
    
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                pair = (points[i], points[j])
                if steps is not None:
                    steps.append(f"    New min: {min_dist:.4f} between {points[i]} and {points[j]}")
    
    if steps is not None:
        steps.append(f"  ✓ Base case result: distance = {min_dist:.4f}")
    return min_dist, pair

def closest_pair_recursive(px, py, depth=0, steps=None):
    """Recursive divide and conquer closest pair"""
    indent = "  " * depth
    n = len(px)
    
    
    # Base case
    if n <= 3:
        return brute_force_closest(px, steps)
    
    # DIVIDE: Split into left and right halves
    mid = n // 2
    mid_x = px[mid][0]
    
    if steps is not None:
        steps.append(f"{indent}DIVIDE: Splitting at x = {mid_x:.2f}")
        steps.append(f"{indent}   Left: {len(px[:mid])} points, Right: {len(px[mid:])} points")
    
    Qx = px[:mid]  # Left half
    Rx = px[mid:]  # Right half
    
    # Create y-sorted lists for left and right
    Qy = [p for p in py if p[0] <= mid_x]
    Ry = [p for p in py if p[0] > mid_x]
    
    # CONQUER: Recursive calls
    if steps is not None:
        steps.append(f"{indent}CONQUER: Solving left half recursively")
    left_min, left_pair = closest_pair_recursive(Qx, Qy, depth + 1, steps)
    
    if steps is not None:
        steps.append(f"{indent} CONQUER: Solving right half recursively")
    right_min, right_pair = closest_pair_recursive(Rx, Ry, depth + 1, steps)
    
    # Find minimum from left and right
    if left_min < right_min:
        min_dist = left_min
        min_pair = left_pair
        if steps is not None:
            steps.append(f"{indent}   Left result is better: {left_min:.4f}")
    else:
        min_dist = right_min
        min_pair = right_pair
        if steps is not None:
            steps.append(f"{indent}   Right result is better: {right_min:.4f}")
    
    # COMBINE: Check strip around midline
    if steps is not None:
        steps.append(f"{indent}COMBINE: Checking strip ±{min_dist:.4f} around x={mid_x:.2f}")
    
    strip = [p for p in py if abs(p[0] - mid_x) < min_dist]
    strip_len = len(strip)
    
    if steps is not None:
        steps.append(f"{indent}   Strip contains {strip_len} points")
    
    # Check points in strip (only need to check next 7 points)
    strip_improved = False
    for i in range(strip_len):
        j = i + 1
        while j < strip_len and (strip[j][1] - strip[i][1]) < min_dist:
            d = distance(strip[i], strip[j])
            if d < min_dist:
                min_dist = d
                min_pair = (strip[i], strip[j])
                strip_improved = True
                if steps is not None:
                    steps.append(f"{indent}   NEW CLOSEST in strip: {strip[i]} ↔ {strip[j]}")
                    steps.append(f"{indent}   New distance: {min_dist:.4f}")
            j += 1
    
    if steps is not None:
        if strip_improved:
            steps.append(f"{indent}Strip improved the result!")
        else:
            steps.append(f"{indent}   Strip didn't improve result")
        steps.append(f"{indent}Level {depth} complete: min_dist = {min_dist:.4f}")
    
    return min_dist, min_pair

def closest_pair(points):
    """Main divide and conquer closest pair algorithm"""
    steps = []
    n = len(points)
    
    if n < 2:
        return None, None, ["Need at least 2 points"]
    
    steps.append(f" Starting Divide & Conquer Closest Pair")
    steps.append(f"   Total points: {n}")
    steps.append(f"   Time Complexity: O(n log n)")
    
    # Pre-sort points by x and y coordinates
    steps.append("   Sorting points by x-coordinate...")
    px = sorted(points, key=lambda p: (p[0], p[1]))
    
    steps.append("   Sorting points by y-coordinate...")
    py = sorted(points, key=lambda p: (p[1], p[0]))
    
    steps.append("   Beginning recursive divide & conquer...")
    steps.append("=" * 50)
    
    min_dist, min_pair = closest_pair_recursive(px, py, 0, steps)
    
    steps.append("=" * 50)
    steps.append(f"   Closest Pair: {min_pair[0]} ↔ {min_pair[1]}")
    steps.append(f"   Minimum Distance: {min_dist:.6f}")
    
    return min_dist, min_pair, steps



def multiply_simple(a, b):
    steps = []
    b_str = str(b)
    partials = []
    
    for i, digit in enumerate(reversed(b_str)):
        partial = a * int(digit) * (10 ** i)
        partials.append(partial)
        steps.append(f"{a} × {digit} (shift {i}) = {partial:,}")
    
    final = sum(partials)
    return final, partials, steps

# ================= CLOSEST PAIR =================
if algo_choice == "Closest Pair of Points":
    st.header("Closest Pair of Points Visualizer")
    
    uploaded_file = st.file_uploader(
        "Upload a text file with points (x y per line):",
        type=["txt"],
        key="closest_pair_file"
    )
    
    if uploaded_file is not None:
        try:
            file_contents = uploaded_file.read().decode("utf-8").splitlines()
            points = []
            
            try:
                n = int(file_contents[0])
                for line in file_contents[1:n+1]:
                    x, y = map(float, line.strip().split())
                    points.append((x, y))
            except:
                for line in file_contents:
                    if line.strip():
                        x, y = map(float, line.strip().split())
                        points.append((x, y))
            
            if len(points) < 2:
                st.warning("Need at least 2 points")
            else:
                # Initialize session state for closest pair
                if 'cp_steps' not in st.session_state:
                    st.session_state.cp_steps = None
                if 'cp_current_step' not in st.session_state:
                    st.session_state.cp_current_step = 0
                if 'cp_auto_play' not in st.session_state:
                    st.session_state.cp_auto_play = False
                if 'cp_result' not in st.session_state:
                    st.session_state.cp_result = None
                
                # Controls
                col1, col2, col3 = st.columns([2, 2, 2])
                with col1:
                    if st.button("Run Algorithm", key="run_cp"):
                        start = time.perf_counter()
                        d, pair, steps = closest_pair(points)
                        elapsed = time.perf_counter() - start
                        st.session_state.cp_steps = steps
                        st.session_state.cp_result = (d, pair, elapsed, points)
                        st.session_state.cp_current_step = 0
                        st.rerun()
                
                with col2:
                    animation_speed = st.select_slider(
                        "Animation Speed",
                        options=["Slow", "Medium", "Fast"],
                        value="Medium",
                        key="cp_speed"
                    )
                
                with col3:
                    if st.session_state.cp_steps:
                        if st.button("▶️ Auto Play" if not st.session_state.cp_auto_play else "⏸️ Pause"):
                            st.session_state.cp_auto_play = not st.session_state.cp_auto_play
                            st.rerun()
                
                speed_map = {"Slow": 1.0, "Medium": 0.5, "Fast": 0.2}
                delay = speed_map[animation_speed]
                
                if st.session_state.cp_result:
                    d, pair, elapsed, pts = st.session_state.cp_result
                    
                    # Results
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Closest Distance", f"{d:.6f}")
                    with col2:
                        st.metric("Pair", f"{pair[0]} ↔ {pair[1]}")
                    with col3:
                        st.metric(" Time", f"{elapsed:.6f}s")
                    
                    st.markdown("---")
                    
                    # Two column layout
                    left_col, right_col = st.columns([1, 1])
                    
                    with left_col:
                        st.subheader("Step-by-Step Process")
                        
                        if st.session_state.cp_steps:
                            total_steps = len(st.session_state.cp_steps)
                            
                            # Navigation
                            nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])
                            
                            with nav_col1:
                                if st.button("⏮️ First", key="cp_first", disabled=(st.session_state.cp_current_step == 0)):
                                    st.session_state.cp_current_step = 0
                                    st.rerun()
                            
                            with nav_col2:
                                if st.button("◀️ Prev", key="cp_prev", disabled=(st.session_state.cp_current_step == 0)):
                                    st.session_state.cp_current_step -= 1
                                    st.rerun()
                            
                            with nav_col3:
                                st.markdown(f"<div style='text-align: center; color: #e0e7ff; padding: 0.5rem;'>Step {st.session_state.cp_current_step + 1} of {total_steps}</div>", unsafe_allow_html=True)
                            
                            with nav_col4:
                                if st.button("Next ▶️", key="cp_next", disabled=(st.session_state.cp_current_step >= total_steps - 1)):
                                    st.session_state.cp_current_step += 1
                                    st.rerun()
                            
                            with nav_col5:
                                if st.button("Last ⏭️", key="cp_last", disabled=(st.session_state.cp_current_step >= total_steps - 1)):
                                    st.session_state.cp_current_step = total_steps - 1
                                    st.rerun()
                            
                            # Display current step
                            current_step = st.session_state.cp_steps[st.session_state.cp_current_step]
                            st.markdown(
                                f"<div class='step-card'>{current_step}</div>",
                                unsafe_allow_html=True
                            )
                            
                            # Auto-play logic
                            if st.session_state.cp_auto_play and st.session_state.cp_current_step < total_steps - 1:
                                time.sleep(delay)
                                st.session_state.cp_current_step += 1
                                st.rerun()
                            elif st.session_state.cp_auto_play and st.session_state.cp_current_step >= total_steps - 1:
                                st.session_state.cp_auto_play = False
                    
                    with right_col:
                        st.subheader("Visualization")
                        
                        # Create figure
                        fig, ax = plt.subplots(figsize=(10, 8))
                        fig.patch.set_facecolor('#0f172a')
                        ax.set_facecolor('#1e293b')
                        
                        xs = [p[0] for p in pts]
                        ys = [p[1] for p in pts]
                        
                        # Plot all points
                        ax.scatter(xs, ys, s=200, c='skyblue', edgecolor='#3b82f6', 
                                  linewidth=2, alpha=0.8, label="All Points", zorder=3)
                        
                        # Highlight closest pair
                        ax.scatter([pair[0][0], pair[1][0]], [pair[0][1], pair[1][1]], 
                                  s=350, c='red', edgecolor='#f472b6', 
                                  linewidth=3, label='Closest Pair', zorder=4)
                        
                        # Draw line
                        ax.plot([pair[0][0], pair[1][0]], [pair[0][1], pair[1][1]], 
                               'r--', linewidth=3, alpha=0.8, zorder=2)
                        
                        # Add distance label
                        mid_x = (pair[0][0] + pair[1][0]) / 2
                        mid_y = (pair[0][1] + pair[1][1]) / 2
                        ax.text(mid_x, mid_y, f'd = {d:.4f}', 
                               fontsize=14, color='yellow', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', 
                                        edgecolor='yellow', linewidth=2),
                               ha='center', va='bottom')
                        
                        ax.legend(fontsize=11, facecolor='#1e293b', edgecolor='#8b5cf6', 
                                 labelcolor='white')
                        ax.set_xlabel("X Coordinate", color='white', fontsize=12, fontweight='bold')
                        ax.set_ylabel("Y Coordinate", color='white', fontsize=12, fontweight='bold')
                        ax.set_title(f"Closest Pair Visualization (Distance = {d:.4f})", 
                                    color='white', fontsize=14, fontweight='bold', pad=15)
                        ax.tick_params(colors='white')
                        ax.grid(True, alpha=0.3, linestyle='--', color='#60a5fa')
                        
                        for spine in ax.spines.values():
                            spine.set_color('#8b5cf6')
                            spine.set_linewidth(2)
                        
                        plt.tight_layout()
                        st.pyplot(fig)
        
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("⬆Please upload a text file to begin")

# ================= INTEGER MULTIPLICATION =================
elif algo_choice == "Integer Multiplication":
    st.header("Integer Multiplication Visualizer - Divide & Conquer")
    
    # Divide and Conquer multiplication functions
    def karatsuba_multiply(x, y, depth=0):
        """Karatsuba divide-and-conquer multiplication algorithm"""
        steps = []
        indent = "  " * depth
        
        # Base case: if numbers are small enough, use regular multiplication
        if x < 10 or y < 10:
            result = x * y
            steps.append(f"{indent}Base case: {x} × {y} = {result}")
            return result, steps
        
        # Calculate the size of the numbers
        n = max(len(str(x)), len(str(y)))
        m = n // 2
        
        # Split the digit sequences in the middle
        high1, low1 = x // (10**m), x % (10**m)
        high2, low2 = y // (10**m), y % (10**m)
        
        steps.append(f"{indent}Splitting: {x} = {high1}×10^{m} + {low1}")
        steps.append(f"{indent}Splitting: {y} = {high2}×10^{m} + {low2}")
        
        # Recursive steps
        steps.append(f"{indent}Computing z0 = {low1} × {low2}")
        z0, steps0 = karatsuba_multiply(low1, low2, depth + 1)
        
        steps.append(f"{indent}Computing z1 = ({low1} + {high1}) × ({low2} + {high2})")
        z1, steps1 = karatsuba_multiply((low1 + high1), (low2 + high2), depth + 1)
        
        steps.append(f"{indent}Computing z2 = {high1} × {high2}")
        z2, steps2 = karatsuba_multiply(high1, high2, depth + 1)
        
        # Combine the results
        result = z2 * (10**(2*m)) + (z1 - z2 - z0) * (10**m) + z0
        
        steps.extend(steps0)
        steps.extend(steps1)
        steps.extend(steps2)
        
        steps.append(f"{indent}Combining: z2×10^{2*m} + (z1-z2-z0)×10^{m} + z0")
        steps.append(f"{indent}Combining: {z2}×10^{2*m} + ({z1}-{z2}-{z0})×10^{m} + {z0}")
        steps.append(f"{indent}Final result: {result}")
        
        return result, steps

    def multiply_with_steps(a, b):
        """Return final product and steps using divide-and-conquer"""
        final, all_steps = karatsuba_multiply(a, b)
        
        # Format steps for display
        formatted_steps = []
        for step in all_steps:
            formatted_steps.append(step)
        
        return final, formatted_steps

    file1 = st.file_uploader("Upload first file (integers, one per line)", 
                             type=["txt"], key="file1")
    file2 = st.file_uploader("Upload second file (integers, one per line)", 
                             type=["txt"], key="file2")
    
    if file1 and file2:
        try:
            # Read files
            numbers1 = [int(line.strip()) for line in file1.read().decode("utf-8").splitlines() if line.strip()]
            numbers2 = [int(line.strip()) for line in file2.read().decode("utf-8").splitlines() if line.strip()]
            
            # Process multiplications
            results = []
            start = time.perf_counter()
            for a, b in zip(numbers1, numbers2):
                final, steps = multiply_with_steps(a, b)
                results.append((a, b, final, steps))
            elapsed = time.perf_counter() - start
            
            # Session state
            if 'mult_current_idx' not in st.session_state:
                st.session_state.mult_current_idx = 0
            if 'mult_current_step' not in st.session_state:
                st.session_state.mult_current_step = 0
            if 'mult_auto_play' not in st.session_state:
                st.session_state.mult_auto_play = False
            
            total_items = len(results)
            
            # Control panel
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.metric("Total Multiplications", total_items)
            with col2:
                st.metric("Total Time", f"{elapsed:.6f}s")
            with col3:
                animation_speed = st.select_slider(
                    "Speed",
                    options=["Slow", "Medium", "Fast"],
                    value="Medium",
                    key="mult_speed"
                )
            
            speed_map = {"Slow": 0.8, "Medium": 0.4, "Fast": 0.2}
            step_delay = speed_map[animation_speed]
            
            st.markdown("---")
            
            # Two column layout
            left_col, right_col = st.columns([1, 1])
            
            with left_col:
                st.subheader("Divide & Conquer Steps")
                
                # Navigation for which multiplication
                nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns([1, 1, 2, 1, 1, 1])
                
                with nav_col1:
                    if st.button("⏮️ First", key="mult_first", disabled=(st.session_state.mult_current_idx == 0)):
                        st.session_state.mult_current_idx = 0
                        st.session_state.mult_current_step = 0
                        st.rerun()
                
                with nav_col2:
                    if st.button("◀️ Prev", key="mult_prev_mult", disabled=(st.session_state.mult_current_idx == 0)):
                        st.session_state.mult_current_idx -= 1
                        st.session_state.mult_current_step = 0
                        st.rerun()
                
                with nav_col3:
                    st.markdown(f"<div style='text-align: center; color: #e0e7ff; padding: 0.5rem;'>Multiplication {st.session_state.mult_current_idx + 1} of {total_items}</div>", unsafe_allow_html=True)
                
                with nav_col4:
                    if st.button("Next ▶️", key="mult_next_mult", disabled=(st.session_state.mult_current_idx >= total_items - 1)):
                        st.session_state.mult_current_idx += 1
                        st.session_state.mult_current_step = 0
                        st.rerun()
                
                with nav_col5:
                    if st.button("Last ⏭️", key="mult_last", disabled=(st.session_state.mult_current_idx >= total_items - 1)):
                        st.session_state.mult_current_idx = total_items - 1
                        st.session_state.mult_current_step = 0
                        st.rerun()
                
                with nav_col6:
                    if st.button("▶️ Auto Play" if not st.session_state.mult_auto_play else "⏸️ Pause"):
                        st.session_state.mult_auto_play = not st.session_state.mult_auto_play
                        st.rerun()
                
                # Current multiplication
                idx = st.session_state.mult_current_idx
                a, b, final, steps = results[idx]
                
                st.markdown(f"""
                <div class="step-card">
                    <h4 style="color: #60a5fa; margin: 0 0 1rem 0;">
                        #{idx + 1}: {a:,} × {b:,} = {final:,}
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Step navigation within current multiplication
                total_steps = len(steps) + 1  # +1 for final summary
                
                step_nav1, step_nav2, step_nav3, step_nav4, step_nav5 = st.columns([1, 1, 2, 1, 1])
                
                with step_nav1:
                    if st.button("⏮️", key="step_first", disabled=(st.session_state.mult_current_step == 0)):
                        st.session_state.mult_current_step = 0
                        st.rerun()
                
                with step_nav2:
                    if st.button("◀️", key="step_prev", disabled=(st.session_state.mult_current_step == 0)):
                        st.session_state.mult_current_step -= 1
                        st.rerun()
                
                with step_nav3:
                    st.markdown(f"<div style='text-align: center; color: #e0e7ff; padding: 0.5rem;'>Step {st.session_state.mult_current_step + 1} of {total_steps}</div>", unsafe_allow_html=True)
                
                with step_nav4:
                    if st.button("▶️", key="step_next", disabled=(st.session_state.mult_current_step >= total_steps - 1)):
                        st.session_state.mult_current_step += 1
                        st.rerun()
                
                with step_nav5:
                    if st.button("⏭️", key="step_last", disabled=(st.session_state.mult_current_step >= total_steps - 1)):
                        st.session_state.mult_current_step = total_steps - 1
                        st.rerun()
                
                # Display current step
                if st.session_state.mult_current_step < len(steps):
                    step_text = steps[st.session_state.mult_current_step]
                    # Add syntax highlighting for different types of steps
                    if "Base case" in step_text:
                        color = "#10b981"  # Green for base cases
                    elif "Splitting" in step_text:
                        color = "#f59e0b"  # Yellow for splitting
                    elif "Computing" in step_text:
                        color = "#3b82f6"  # Blue for recursive calls
                    elif "Combining" in step_text:
                        color = "#ec4899"  # Pink for combining
                    else:
                        color = "#c7d2fe"  # Default
                    
                    st.markdown(f"""
                    <div class="step-card">
                        <div style="color: {color}; font-family: 'Courier New', monospace; font-size: 0.95rem; line-height: 1.6;">
                            {step_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Final summary
                    st.markdown(f"""
                    <div class="step-card">
                        <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid rgba(96, 165, 250, 0.3);">
                            <strong style="color: #ec4899; font-size: 1.2rem;">✓ Multiplication Complete!</strong><br>
                            <strong style="color: #10b981; font-size: 1.1rem;">Final Product: {final:,}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Auto-play logic
                if st.session_state.mult_auto_play:
                    time.sleep(step_delay)
                    if st.session_state.mult_current_step < total_steps - 1:
                        st.session_state.mult_current_step += 1
                        st.rerun()
                    elif st.session_state.mult_current_idx < total_items - 1:
                        st.session_state.mult_current_idx += 1
                        st.session_state.mult_current_step = 0
                        st.rerun()
                    else:
                        st.session_state.mult_auto_play = False
                        st.rerun()
            
            with right_col:
                st.subheader("Algorithm Analysis")
                
                # Statistics
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.write("**Statistics:**")
                products = [final for _, _, final, _ in results]
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Max Product", f"{max(products):,}")
                    st.metric("Min Product", f"{min(products):,}")
                with col_b:
                    st.metric("Average", f"{np.mean(products):,.0f}")
                    st.metric("Median", f"{np.median(products):,.0f}")
                st.markdown("</div>", unsafe_allow_html=True)
              
                
                # Visualization
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.write("**Performance Analysis:**")
                
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
                fig.patch.set_facecolor('#0f172a')
                
                # Plot 1: Product values
                ax1.set_facecolor('#1e293b')
                indices = range(1, len(results) + 1)
                products = [final for _, _, final, _ in results]
                
                bars = ax1.bar(indices, products, color='#60a5fa', alpha=0.8, 
                              edgecolor='#3b82f6', linewidth=1.5)
                
                # Highlight current multiplication
                if results:
                    current_idx = st.session_state.mult_current_idx
                    bars[current_idx].set_color('#ec4899')
                    bars[current_idx].set_edgecolor('#f472b6')
                    bars[current_idx].set_linewidth(3)
                
                ax1.set_xlabel("Multiplication #", color='white', fontsize=12, fontweight='bold')
                ax1.set_ylabel("Product Value", color='white', fontsize=12, fontweight='bold')
                ax1.set_title("Multiplication Results", color='white', fontsize=14, fontweight='bold', pad=15)
                ax1.tick_params(colors='white', labelsize=10)
                ax1.grid(axis='y', alpha=0.3, linestyle='--', color='#60a5fa')
                
                # Plot 2: Histogram
                ax2.set_facecolor('#1e293b')
                if len(products) > 1:
                    n, bins, patches = ax2.hist(products, bins=min(15, len(products)//2 or 1), 
                            color='#10b981', alpha=0.8, edgecolor='white', linewidth=1.5)
                    
                    # Color gradient
                    for i, patch in enumerate(patches):
                        patch.set_facecolor(plt.cm.viridis(i / len(patches)))
                
                ax2.set_xlabel("Product Value", color='white', fontsize=12, fontweight='bold')
                ax2.set_ylabel("Frequency", color='white', fontsize=12, fontweight='bold')
                ax2.set_title("Product Distribution", color='white', fontsize=14, fontweight='bold', pad=15)
                ax2.tick_params(colors='white', labelsize=10)
                ax2.grid(axis='both', alpha=0.3, linestyle='--', color='#60a5fa')
                
                for ax in [ax1, ax2]:
                    for spine in ax.spines.values():
                        spine.set_color('#8b5cf6')
                        spine.set_linewidth(2)
                
                plt.tight_layout()
                st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("⬆Please upload both files to begin")