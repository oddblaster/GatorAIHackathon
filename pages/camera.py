import streamlit as st
import cv2
import numpy as np
import socket
import geopy
import json
import os
from supabase import Client, create_client
from dotenv import load_dotenv
from requests import get

load_dotenv()
IPAPI_KEY = os.getenv("IPAPI_KEY")

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

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
        cv2.imwrite("saved.jpeg", frame)
        cap.release()

        # get users public ip address and extract lat and long data from that
        ip = get('https://api.ipify.org').text
        # st.write('My public IP address is: {}'.format(ip))

        url = f'https://api.ipapi.com/api/{ip}?access_key={IPAPI_KEY}&fields=latitude,longitude'
        response = get(url)
        data = response.json()

        st.write(data)
        
        response = supabase.table("input_data").insert({"latitude":data["latitude"], "longitude":data["longitude"], "text_description":"POOPOOPEEPEE"}).execute()