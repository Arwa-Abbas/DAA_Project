from backend.closest_pair import closest_pair
import streamlit as st
import matplotlib.pyplot as plt
from backend.closest_pair import read_points_from_file, closest_pair
import time

st.set_page_config(page_title="DAA Project", layout="wide")


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
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
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
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Premium glass morphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(30, 27, 75, 0.7) !important;
        backdrop-filter: blur(30px) saturate(180%);
        border-right: 2px solid rgba(139, 92, 246, 0.3);
        box-shadow: 8px 0 40px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 200px;
        background: linear-gradient(180deg, 
            rgba(139, 92, 246, 0.2) 0%, 
            transparent 100%);
        pointer-events: none;
    }
    
    [data-testid="stSidebar"] label {
        color: #e0e7ff !important;
        font-weight: 700;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    /* Animated selectbox */
    .stSelectbox > div > div {
        background: rgba(59, 130, 246, 0.15) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(139, 92, 246, 0.4) !important;
        border-radius: 12px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .stSelectbox > div > div:hover {
        background: rgba(139, 92, 246, 0.25) !important;
        border: 1px solid rgba(167, 139, 250, 0.6) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.4);
    }
    
    /* Premium glass file uploader with glow */
    [data-testid="stFileUploader"] {
        background: rgba(30, 58, 138, 0.2);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        padding: 2.5rem;
        border: 2px solid rgba(139, 92, 246, 0.3);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4),
                    0 0 60px rgba(139, 92, 246, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: slideInLeft 0.8s ease-out, pulseGlow 3s ease-in-out infinite;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stFileUploader"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(139, 92, 246, 0.1),
            transparent
        );
        animation: scanline 3s linear infinite;
    }
    
    @keyframes scanline {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(59, 130, 246, 0.25);
        border: 2px solid rgba(167, 139, 250, 0.5);
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 12px 50px rgba(139, 92, 246, 0.4),
                    0 0 80px rgba(167, 139, 250, 0.3);
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-80px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4),
                        0 0 60px rgba(139, 92, 246, 0.2);
        }
        50% { 
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4),
                        0 0 80px rgba(167, 139, 250, 0.4);
        }
    }
    
    [data-testid="stFileUploader"] label {
        color: #e0e7ff !important;
        font-weight: 700;
        font-size: 1.15rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stFileUploader"] small {
        color: #c7d2fe !important;
        font-weight: 500;
    }
    
    /* Dashboard-style alert boxes with animations */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
        border-left: 4px solid #10b981 !important;
        border-right: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-top: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-bottom: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #d1fae5 !important;
        animation: slideInUp 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 4px 24px rgba(16, 185, 129, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        font-weight: 600;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
        border-left: 4px solid #3b82f6 !important;
        border-right: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-top: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #dbeafe !important;
        animation: slideInUp 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 4px 24px rgba(59, 130, 246, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        font-weight: 600;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
        border-left: 4px solid #f59e0b !important;
        border-right: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-top: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-bottom: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #fef3c7 !important;
        animation: slideInUp 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 4px 24px rgba(245, 158, 11, 0.3);
        font-weight: 600;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
        border-left: 4px solid #ef4444 !important;
        border-right: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-top: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-bottom: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #fee2e2 !important;
        animation: slideInUp 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 4px 24px rgba(239, 68, 68, 0.3);
        font-weight: 600;
    }
    
    @keyframes slideInUp {
        0% {
            transform: translateY(30px) scale(0.95);
            opacity: 0;
        }
        50% {
            transform: translateY(-5px) scale(1.02);
        }
        100% {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
    }
    
    /* Plot container with glass card effect */
    .element-container:has(.stPlotlyChart) {
        animation: zoomIn 0.8s ease-out;
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4),
                    0 0 60px rgba(59, 130, 246, 0.2);
    }
    
    @keyframes zoomIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Loading spinner with neon effect */
    .stSpinner > div {
        border-color: #8b5cf6 !important;
        border-right-color: transparent !important;
        animation: spin 0.8s linear infinite, neonPulse 1.5s ease-in-out infinite;
    }
    
    @keyframes neonPulse {
        0%, 100% { 
            filter: drop-shadow(0 0 8px #8b5cf6);
        }
        50% { 
            filter: drop-shadow(0 0 16px #a78bfa);
        }
    }
    
    /* Hover effects for interactive elements */
    button {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(139, 92, 246, 0.4);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 27, 75, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #8b5cf6, #3b82f6);
        border-radius: 10px;
        border: 2px solid rgba(30, 27, 75, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #a78bfa, #60a5fa);
    }
</style>
""", unsafe_allow_html=True)

st.title("Divide & Conquer Algorithms")

# Sidebar for algorithm selection
algo_choice = st.sidebar.selectbox(
    "Select Algorithm",
    ["Closest Pair of Points"] 
)

if algo_choice == "Closest Pair of Points":
    st.header("Closest Pair of Points")

    # File uploader
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