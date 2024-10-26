import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="Camera Snapshot",
    page_icon="📷",
)

st.title("Take a Picture")

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
