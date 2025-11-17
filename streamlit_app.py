import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Hand Gesture Recognition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    /* Main styling */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #2196F3 0%, #FF5722 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .header-container h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        color: white;
        font-weight: 700;
    }
    
    .header-container p {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
    }
    
    /* Video container */
    .video-container {
        background: #1a1a1a;
        border: 2px solid #333333;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .video-container:hover {
        border-color: #2196F3;
        box-shadow: 0 12px 48px rgba(33, 150, 243, 0.2);
    }
    
    /* Gesture display */
    .gesture-display {
        font-size: 4rem;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(255, 87, 34, 0.1) 100%);
        border-radius: 15px;
        color: #2196F3;
        font-weight: 700;
        border: 2px solid rgba(33, 150, 243, 0.3);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .gesture-display:hover {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.2) 0%, rgba(255, 87, 34, 0.2) 100%);
        border-color: #2196F3;
        transform: scale(1.02);
    }
    
    /* Info cards */
    .info-card {
        background: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        border-color: #2196F3;
        background: rgba(33, 150, 243, 0.05);
    }
    
    .info-card h2 {
        color: #2196F3;
        margin-bottom: 1rem;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    /* Gesture items */
    .gesture-item {
        background: rgba(33, 150, 243, 0.1);
        border: 1px solid rgba(33, 150, 243, 0.2);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .gesture-item:hover {
        background: rgba(33, 150, 243, 0.2);
        border-color: #2196F3;
        transform: translateY(-5px);
    }
    
    .gesture-icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .gesture-name {
        color: #b0b0b0;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Status indicators */
    .status-active {
        background: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-inactive {
        background: rgba(158, 158, 158, 0.2);
        color: #9e9e9e;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976D2 0%, #0d47a1 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(33, 150, 243, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #333;
    }
    
    .footer a {
        color: #2196F3;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Instructions */
    .instructions-list {
        list-style: none;
        padding: 0;
    }
    
    .instructions-list li {
        padding: 0.75rem 0;
        padding-left: 2rem;
        position: relative;
        color: #b0b0b0;
    }
    
    .instructions-list li:before {
        content: "→";
        position: absolute;
        left: 0;
        color: #2196F3;
        font-weight: bold;
    }
    
    /* Divider */
    .divider {
        background: linear-gradient(90deg, transparent, #333, transparent);
        height: 1px;
        margin: 2rem 0;
    }
    
    </style>
""", unsafe_allow_html=True)

# Initialize MediaPipe
@st.cache_resource
def init_mediapipe():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    return mp_hands, hands

mp_hands, hands = init_mediapipe()
mp_draw = mp.solutions.drawing_utils

def get_finger_status(hand_landmarks):
    """Determine which fingers are open or closed"""
    finger_tips = [8, 12, 16, 20]
    finger_mcp = [5, 9, 13, 17]
    status = []
    
    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        status.append(1)
    else:
        status.append(0)
    
    # Other fingers
    for tip, mcp in zip(finger_tips, finger_mcp):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y:
            status.append(1)
        else:
            status.append(0)
    
    return status

def recognize_gesture(finger_status):
    """Recognize gesture from finger status"""
    gestures = {
        tuple([0,1,0,0,0]): "Peace ✌️",
        tuple([1,1,1,1,1]): "Open Hand 🖐️",
        tuple([0,0,0,0,0]): "Thumbs Up ✊",
        tuple([1,0,0,0,0]): "Fist 👍"
    }
    return gestures.get(tuple(finger_status), "Unknown ❓")

def process_frame(frame):
    """Process frame and detect gestures"""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    gesture_text = "No hands detected"
    hand_count = 0
    detected_gestures = []
    
    if results.multi_hand_landmarks:
        hand_count = len(results.multi_hand_landmarks)
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            # Recognize gesture
            finger_status = get_finger_status(hand_landmarks)
            gesture = recognize_gesture(finger_status)
            detected_gestures.append(gesture)
        
        gesture_text = detected_gestures[0] if detected_gestures else "Unknown"
    
    return frame, gesture_text, hand_count, detected_gestures

# Initialize session state
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

if "frame_count" not in st.session_state:
    st.session_state.frame_count = 0

if "gesture_history" not in st.session_state:
    st.session_state.gesture_history = []

# Header
st.markdown("""
    <div class="header-container">
        <h1>🤖 Hand Gesture Recognition</h1>
        <p>Real-time gesture detection powered by AI & MediaPipe</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    camera_choice = st.selectbox(
        "Select Camera",
        [0, 1, 2],
        help="Your primary camera is usually 0"
    )
    
    st.divider()
    st.subheader("📋 Supported Gestures")
    
    gestures_guide = {
        "✌️ Peace": "Index & middle finger up",
        "🖐️ Open Hand": "All 5 fingers open",
        "✊ Thumbs Up": "Only thumb up",
        "👍 Fist": "All fingers closed"
    }
    
    for gesture, desc in gestures_guide.items():
        st.caption(f"**{gesture}**\n{desc}")
    
    st.divider()
    
    st.subheader("📊 Stats")
    st.metric("Frames Processed", st.session_state.frame_count)
    
    if st.session_state.gesture_history:
        most_common = max(set(st.session_state.gesture_history), 
                         key=st.session_state.gesture_history.count)
        st.metric("Most Detected Gesture", most_common)

# Main content
col1, col2 = st.columns([2.5, 1.5], gap="large")

with col1:
    st.subheader("📹 Live Camera Feed", divider="blue")
    
    # Placeholders
    frame_placeholder = st.empty()
    gesture_placeholder = st.empty()
    
    # Control buttons
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        start_btn = st.button("🎬 Start Camera", key="start", use_container_width=True)
    
    with btn_col2:
        stop_btn = st.button("⏹️ Stop Camera", key="stop", use_container_width=True)
    
    with btn_col3:
        reset_btn = st.button("🔄 Reset Stats", key="reset", use_container_width=True)
    
    if start_btn:
        st.session_state.camera_active = True
    
    if stop_btn:
        st.session_state.camera_active = False
    
    if reset_btn:
        st.session_state.frame_count = 0
        st.session_state.gesture_history = []
        st.rerun()
    
    # Camera feed loop
    if st.session_state.camera_active:
        camera = cv2.VideoCapture(camera_choice)
        
        if not camera.isOpened():
            st.error("❌ Cannot access camera. Check if it's connected and not in use.")
        else:
            st.success("✅ Camera connected!")
            
            # Frame display area
            video_display = frame_placeholder.container()
            gesture_display = gesture_placeholder.container()
            
            # Process frames
            frame_window = st.empty()
            
            while st.session_state.camera_active:
                ret, frame = camera.read()
                
                if not ret:
                    st.error("Failed to read camera frame")
                    break
                
                # Resize for faster processing
                frame = cv2.resize(frame, (640, 480))
                frame = cv2.flip(frame, 1)
                
                # Process
                processed_frame, gesture, hand_count, all_gestures = process_frame(frame)
                
                # Add text overlay
                cv2.putText(
                    processed_frame,
                    gesture,
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (0, 255, 0),
                    3
                )
                
                cv2.putText(
                    processed_frame,
                    f"Hands: {hand_count}",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )
                
                # Display
                frame_placeholder.image(processed_frame, channels="BGR", use_column_width=True)
                
                # Display gesture with styling
                if gesture != "No hands detected":
                    gesture_placeholder.markdown(f"""
                        <div class="gesture-display">
                            {gesture}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    gesture_placeholder.markdown("""
                        <div class="gesture-display" style="color: #999;">
                            Waiting for hands...
                        </div>
                    """, unsafe_allow_html=True)
                
                # Update stats
                st.session_state.frame_count += 1
                if gesture != "No hands detected":
                    st.session_state.gesture_history.append(gesture)
                
                time.sleep(0.033)  # ~30 FPS
            
            camera.release()

with col2:
    st.subheader("📊 Information", divider="blue")
    
    # Status
    st.markdown("**Status**")
    if st.session_state.camera_active:
        st.markdown('<p class="status-active">🟢 Camera Active</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-inactive">⚫ Camera Inactive</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # Quick stats
    st.markdown("**Quick Stats**")
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Frames</div>
            <div class="metric-value">{st.session_state.frame_count}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Unique Gestures</div>
            <div class="metric-value">{len(set(st.session_state.gesture_history))}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gesture guide
    st.markdown("**🎯 Gesture Guide**")
    
    for emoji_gesture, description in gestures_guide.items():
        st.markdown(f"""
        <div class="gesture-item">
            <div class="gesture-icon">{emoji_gesture.split()[0]}</div>
            <div class="gesture-name"><b>{emoji_gesture}</b><br>{description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # How to use
    st.markdown("**📖 How to Use**")
    st.markdown("""
    <ul class="instructions-list">
        <li>Click "Start Camera"</li>
        <li>Show your hands</li>
        <li>Make gestures</li>
        <li>See results in real-time</li>
    </ul>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>Hand Gesture Recognition • Built with Streamlit & MediaPipe</p>
        <p>© 2025 • <a href="#">GitHub</a> • <a href="#">Documentation</a></p>
    </div>
""", unsafe_allow_html=True)
