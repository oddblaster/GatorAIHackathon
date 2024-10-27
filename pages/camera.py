import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="Camera Snapshot",
    page_icon="📷",
    layout="wide"
)

st.title("Take a Picture")


html_string = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  	<script src="https://cdn.tailwindcss.com"></script>
</head>
<style>
    .text-drop-shadow {
        display: inline-block;
        color: #39FF14;
        font-size: 6rem;
        font-weight: bold;
        filter: drop-shadow(0 0 10px #39FF14);
        margin-right: 2rem; 
    }

         display: inline-block;
        white-space: nowrap;
    }

    .marquee-container {
        overflow: hidden;
        width: 100%;
        background-color: #000000;
        display: flex;
        align-items: center;
    }

    .marquee-content {
        display: flex;
        width: calc(200% + 8rem); /* 200% width plus total margin-right */
        animation: scroll-left 20s linear infinite;
    }

    @keyframes scroll-left {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(-50%);
        }
    }
</style>

<body>
    <div class="marquee-container h-full bg-black">
        <div class="marquee-content">
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
        </div>
    </div>
</body>
"""
st.components.v1.html(html_string, height=360)

# Initialize session state for capturing the image
if "captured_image" not in st.session_state:
    st.session_state["captured_image"] = None

# Access the camera
cap = cv2.VideoCapture(0)

# Initialize a placeholder for the video feed
frame_placeholder = st.empty()

# Take Picture button outside the loop
take_picture = st.button("Take Picture")

# Continuously display video feed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.write("Failed to grab frame.")
        break
    
    # Convert frame to RGB (from BGR) for Streamlit
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Show the video feed in the placeholder
    frame_placeholder.image(frame_rgb, use_column_width=True)

    # Capture image if the button was clicked
    if take_picture:
        st.session_state["captured_image"] = frame
        cv2.imwrite("saved.png", frame)
        cap.release()
