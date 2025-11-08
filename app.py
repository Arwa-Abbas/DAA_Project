import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from backend.closest_pair import closest_pair
from backend.closest_pair import read_points_from_file
from backend.integer_mult import multiply_files, format_steps

st.set_page_config(page_title="DAA Project", layout="wide")

# --- YOUR EXISTING CSS AND STYLING ---
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
    
    /* Title with neon glow and typing effect */
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
    
    /* Header with glass morphism */
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
    
    /* Premium glass morphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(30, 27, 75, 0.7) !important;
        backdrop-filter: blur(30px) saturate(180%);
        border-right: 2px solid rgba(139, 92, 246, 0.3);
        box-shadow: 8px 0 40px rgba(0, 0, 0, 0.5);
    }
    
    /* ... keep rest of your CSS from previous code ... */
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

    file1 = st.file_uploader("Upload first file with integers (one per line)", type=["txt"])
    file2 = st.file_uploader("Upload second file with integers (one per line)", type=["txt"])

    if file1 and file2:
        try:
            # Save uploaded files temporarily
            with open("temp_file1.txt", "wb") as f:
                f.write(file1.getbuffer())
            with open("temp_file2.txt", "wb") as f:
                f.write(file2.getbuffer())

            results, elapsed = multiply_files("temp_file1.txt", "temp_file2.txt")

            # Show step-by-step in Streamlit
            st.subheader("Multiplication Steps")
            for a, b, final, partials in results:
                st.text(format_steps(a, b, final, partials))

            st.info(f"Total time taken: {elapsed:.6f} seconds")

            # Show bar chart in Streamlit
            labels = [f"{a}x{b}" for a, b, _, _ in results]
            products = [final for _, _, final, _ in results]
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(np.arange(len(labels)), products, color='skyblue', edgecolor='navy', alpha=0.7)
            ax.set_xticks(np.arange(len(labels)))
            ax.set_xticklabels(labels, rotation=90, ha='right', fontsize=4)
            ax.set_ylabel("Product (A*B)")
            ax.set_title("Integer Multiplication Results")
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error processing files: {e}")
