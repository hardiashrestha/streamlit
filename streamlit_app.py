import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np

# Page config
st.set_page_config(
    page_title="Hand Gesture Recognition",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
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
    }
    
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
    }
    
    .info-card {
        background: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .gesture-item {
        background: rgba(33, 150, 243, 0.1);
        border: 1px solid rgba(33, 150, 243, 0.2);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .gesture-icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1>🤖 Hand Gesture Recognition</h1>
        <p>Real-time gesture detection powered by AI</p>
    </div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("📹 Live Camera Feed")
    
    st.info("""
    ℹ️ **Note:** This is a demo version running on cloud. 
    For full real-time gesture detection, **run locally** with:
    ```
    streamlit run streamlit_app.py
    ```
    """)
    
    # WebRTC configuration
    rtc_configuration = {
        "iceServers": [
            {"urls": ["stun:stun1.l.google.com:19302"]}
        ]
    }
    
    class VideoProcessor:
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            
            # Flip the image
            img = cv2.flip(img, 1)
            
            # Add placeholder text
            cv2.putText(
                img,
                "Camera Active - Local Version Required",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                2
            )
            
            return av.VideoFrame.from_ndarray(img, format="bgr24")
    
    # WebRTC streamer
    webrtc_streamer(
        key="gesture-recognition",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

with col2:
    st.subheader("📊 Information")
    
    st.markdown("""
    <div class="info-card">
        <h3>🎯 Supported Gestures</h3>
    </div>
    """, unsafe_allow_html=True)
    
    gestures = {
        "✌️": "Peace",
        "🖐️": "Open Hand",
        "✊": "Thumbs Up",
        "👍": "Fist"
    }
    
    for emoji, name in gestures.items():
        st.markdown(f"""
        <div class="gesture-item">
            <div class="gesture-icon">{emoji}</div>
            <div>{name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class="info-card">
        <h3>📖 How to Use Locally</h3>
        <p><strong>1.</strong> Clone the repo from GitHub</p>
        <p><strong>2.</strong> Install: pip install -r requirements.txt</p>
        <p><strong>3.</strong> Run: streamlit run streamlit_app.py</p>
        <p><strong>4.</strong> Open http://localhost:8501</p>
        <p><strong>5.</strong> Start camera and show gestures</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
    <p style="text-align: center; color: #999;">
        Hand Gesture Recognition • Built with Streamlit & MediaPipe
    </p>
""", unsafe_allow_html=True)
