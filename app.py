import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from backend.closest_pair import closest_pair
from backend.closest_pair import read_points_from_file
from backend.integer_mult import multiply_files, format_steps

st.set_page_config(page_title="DAA Project", layout="wide")

# Enhanced CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated gradient background with purple-blue theme */
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
    
    /* Floating particles effect */
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
    
    /* Title with neon glow */
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
        animation: neonGlow 3s ease-in-out infinite,
                   gradientShift 4s ease infinite,
                   fadeInDown 1s ease-out;
        text-shadow: 0 0 30px rgba(96, 165, 250, 0.5),
                     0 0 60px rgba(167, 139, 250, 0.3);
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
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
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
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: slideInRight 0.8s ease-out;
        margin: 1.5rem 0 !important;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    [data-testid="stSidebar"] {
        background: rgba(30, 27, 75, 0.7) !important;
        backdrop-filter: blur(30px) saturate(180%);
        border-right: 2px solid rgba(139, 92, 246, 0.3);
        box-shadow: 8px 0 40px rgba(0, 0, 0, 0.5);
    }
    
    /* Step card animation */
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
    
    /* Result box */
    .result-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(167, 139, 250, 0.15));
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 2px solid rgba(96, 165, 250, 0.4);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(96, 165, 250, 0.3);
        border-radius: 50%;
        border-top-color: #60a5fa;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Pagination button */
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

# Sidebar for algorithm selection
algo_choice = st.sidebar.selectbox(
    "Select Algorithm",
    ["Closest Pair of Points", "Integer Multiplication"]
)

# ------------------- Closest Pair -------------------
if algo_choice == "Closest Pair of Points":
    st.header("Closest Pair of Points")

    uploaded_file = st.file_uploader(
        "Upload a text file with points (x y per line)",
        type=["txt"]
    )

    if uploaded_file is not None:
        try:
            file_contents = uploaded_file.read().decode("utf-8").splitlines()
            points = []
            first_line = file_contents[0]
            try:
                n = int(first_line)
                for line in file_contents[1:n+1]:
                    x, y = map(float, line.strip().split())
                    points.append((x, y))
            except:
                for line in file_contents:
                    if line.strip():
                        x, y = map(float, line.strip().split())
                        points.append((x, y))
            
            if len(points) < 2:
                st.warning("Need at least 2 points to compute closest pair.")
            else:
                start = time.perf_counter()
                result = closest_pair(points)
                elapsed = time.perf_counter() - start
                d, pair = result

                st.success(f"Closest pair: {pair[0]} , {pair[1]}")
                st.info(f"Distance: {d:.6f}")
                st.info(f"Time taken: {elapsed:.6f} seconds")

                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                fig, ax = plt.subplots(figsize=(12, 7))
                
                fig.patch.set_facecolor('#0f172a')
                ax.set_facecolor('#1e293b')
                
                ax.scatter(xs, ys, s=100, color='#3b82f6', alpha=0.6, 
                           edgecolors='#60a5fa', linewidth=2)
                
                ax.scatter([pair[0][0], pair[1][0]], [pair[0][1], pair[1][1]], 
                           s=300, color='#ec4899', alpha=0.9,
                           edgecolors='#f472b6', linewidth=3, zorder=5)
                
                ax.plot([pair[0][0], pair[1][0]], [pair[0][1], pair[1][1]], 
                        color='#f472b6', linewidth=4, linestyle='--', alpha=0.8,
                        solid_capstyle='round')
   
                ax.set_title(f"Closest distance: {d:.6f}", 
                             color='#e0e7ff', fontsize=16, fontweight='bold', 
                             pad=20, family='sans-serif')
                ax.set_xlabel("X Coordinate", color='#c7d2fe', fontsize=12, 
                              fontweight='bold', family='sans-serif')
                ax.set_ylabel("Y Coordinate", color='#c7d2fe', fontsize=12, 
                              fontweight='bold', family='sans-serif')
                ax.tick_params(colors='#a5b4fc', labelsize=10)
                ax.grid(True, alpha=0.15, linestyle='--', color='#60a5fa', linewidth=0.5)
                
                for spine in ax.spines.values():
                    spine.set_color('#8b5cf6')
                    spine.set_linewidth(2)
                
                plt.tight_layout()
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error reading file: {e}")

# ------------------- Integer Multiplication -------------------
elif algo_choice == "Integer Multiplication":
    st.header("Integer Multiplication (Step-by-Step)")

    file1 = st.file_uploader("Upload first file with integers (one per line)", type=["txt"], key="file1")
    file2 = st.file_uploader("Upload second file with integers (one per line)", type=["txt"], key="file2")

    if file1 and file2:
        try:
            # Save uploaded files temporarily
            with open("temp_file1.txt", "wb") as f:
                f.write(file1.getbuffer())
            with open("temp_file2.txt", "wb") as f:
                f.write(file2.getbuffer())

            # Processing indicator
            with st.spinner('🔄 Processing multiplications...'):
                results, elapsed = multiply_files("temp_file1.txt", "temp_file2.txt")

            # Initialize session state for pagination
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 0
            if 'items_per_page' not in st.session_state:
                st.session_state.items_per_page = 10

            total_items = len(results)
            total_pages = (total_items + st.session_state.items_per_page - 1) // st.session_state.items_per_page

            # Control panel
            col1, col2, col3 = st.columns([2, 3, 2])
            
            with col1:
                st.metric("Total Multiplications", total_items)
            with col2:
                st.metric("Total Time", f"{elapsed:.6f}s")
            with col3:
                items_per_page = st.selectbox(
                    "Items per page:",
                    [5, 10, 20, 50, 100],
                    index=1,
                    key="items_select"
                )
                st.session_state.items_per_page = items_per_page

            # Recalculate pages if items_per_page changed
            total_pages = (total_items + st.session_state.items_per_page - 1) // st.session_state.items_per_page
            if st.session_state.current_page >= total_pages:
                st.session_state.current_page = 0

            st.markdown("---")

            # Two column layout
            left_col, right_col = st.columns([1, 1])

            with left_col:
                st.subheader("Multiplication Steps")
                
                # Pagination controls
                nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])
                
                with nav_col1:
                    if st.button("⏮️ First", disabled=(st.session_state.current_page == 0)):
                        st.session_state.current_page = 0
                        st.rerun()
                
                with nav_col2:
                    if st.button("◀️ Prev", disabled=(st.session_state.current_page == 0)):
                        st.session_state.current_page -= 1
                        st.rerun()
                
                with nav_col3:
                    st.markdown(f"<div style='text-align: center; color: #e0e7ff; padding: 0.5rem;'>Page {st.session_state.current_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
                
                with nav_col4:
                    if st.button("Next ▶️", disabled=(st.session_state.current_page >= total_pages - 1)):
                        st.session_state.current_page += 1
                        st.rerun()
                
                with nav_col5:
                    if st.button("Last ⏭️", disabled=(st.session_state.current_page >= total_pages - 1)):
                        st.session_state.current_page = total_pages - 1
                        st.rerun()

                # Display steps for current page with animation delay
                start_idx = st.session_state.current_page * st.session_state.items_per_page
                end_idx = min(start_idx + st.session_state.items_per_page, total_items)
                
                step_container = st.container()
                with step_container:
                    for idx in range(start_idx, end_idx):
                        a, b, final, partials = results[idx]
                        
                        # Animated step card
                        st.markdown(f"""
                        <div class="step-card" style="animation-delay: {(idx - start_idx) * 0.1}s;">
                            <h4 style="color: #60a5fa; margin: 0 0 0.5rem 0;">
                                #{idx + 1}: {a} × {b}
                            </h4>
                            <div style="color: #c7d2fe; font-size: 0.9rem; line-height: 1.6;">
                        """, unsafe_allow_html=True)
                        
                        b_str = str(b)
                        for i, p in enumerate(partials):
                            st.markdown(f"<div style='margin-left: 1rem;'>→ {a} × {b_str[-(i+1)]} (shift {i}) = {p:,}</div>", unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            </div>
                            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(96, 165, 250, 0.3);">
                                <strong style="color: #ec4899; font-size: 1.1rem;">Final Product: {final:,}</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Small delay for animation effect
                        time.sleep(0.05)

            with right_col:
                st.subheader("Results Overview")
                
                # Quick jump to result
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.write("**Quick Jump to Result:**")
                jump_to = st.number_input(
                    "Enter result number (1-" + str(total_items) + "):",
                    min_value=1,
                    max_value=total_items,
                    value=start_idx + 1,
                    step=1
                )
                
                if st.button("Go to Result"):
                    target_page = (jump_to - 1) // st.session_state.items_per_page
                    st.session_state.current_page = target_page
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Summary statistics
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.write("**Summary Statistics:**")
                products = [final for _, _, final, _ in results]
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Max Product", f"{max(products):,}")
                    st.metric("Min Product", f"{min(products):,}")
                with col_b:
                    st.metric("Average", f"{np.mean(products):,.0f}")
                    st.metric("Median", f"{np.median(products):,.0f}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Enhanced visualization
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.write("**Product Distribution:**")
                
                labels = [f"{a}×{b}" for a, b, _, _ in results]
                products = [final for _, _, final, _ in results]
                
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
                
                # Bar chart with gradient
                fig.patch.set_facecolor('#0f172a')
                ax1.set_facecolor('#1e293b')
                
                colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(products)))
                bars = ax1.bar(np.arange(len(labels)), products, color=colors, 
                              edgecolor='#60a5fa', alpha=0.8, linewidth=1.5)
                
                ax1.set_xticks(np.arange(len(labels)))
                ax1.set_xticklabels(labels, rotation=90, ha='right', fontsize=8, color='#c7d2fe')
                ax1.set_ylabel("Product Value", color='#c7d2fe', fontsize=12, fontweight='bold')
                ax1.set_title("All Multiplication Results", color='#e0e7ff', fontsize=14, fontweight='bold', pad=15)
                ax1.tick_params(colors='#a5b4fc', labelsize=9)
                ax1.grid(axis='y', alpha=0.2, linestyle='--', color='#60a5fa')
                
                for spine in ax1.spines.values():
                    spine.set_color('#8b5cf6')
                    spine.set_linewidth(2)
                
                # Histogram
                ax2.set_facecolor('#1e293b')
                ax2.hist(products, bins=min(20, len(products)//2 or 1), 
                        color='#ec4899', alpha=0.7, edgecolor='#f472b6', linewidth=2)
                ax2.set_xlabel("Product Value", color='#c7d2fe', fontsize=12, fontweight='bold')
                ax2.set_ylabel("Frequency", color='#c7d2fe', fontsize=12, fontweight='bold')
                ax2.set_title("Product Distribution", color='#e0e7ff', fontsize=14, fontweight='bold', pad=15)
                ax2.tick_params(colors='#a5b4fc', labelsize=9)
                ax2.grid(axis='both', alpha=0.2, linestyle='--', color='#60a5fa')
                
                for spine in ax2.spines.values():
                    spine.set_color('#8b5cf6')
                    spine.set_linewidth(2)
                
                plt.tight_layout()
                st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error processing files: {e}")
