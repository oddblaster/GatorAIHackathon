import streamlit as st
import cv2
import numpy as np
import socket
import geopy
import json
import os
from geopy.geocoders import Nominatim
from supabase import Client, create_client
from dotenv import load_dotenv
from requests import get
from uuid import uuid4

load_dotenv()

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

st.set_page_config(
    page_title="Camera Snapshot",
    page_icon="📷",
    layout="wide"
)

st.title("Take a Picture of How You Were Affected 📷")

html_string = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  	<script src="https://cdn.tailwindcss.com"></script>
    <style>
        .text-drop-shadow {
            display: inline-block;
            color: #39FF14;
            font-size: 6rem;
            font-weight: bold;
            filter: drop-shadow(0 0 10px #39FF14);
            margin-right: 2rem; 
        }

        .scrolling-text {
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
            width: 200%;
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
</head>

<body>
    <div class="marquee-container h-full bg-black">
        <div class="marquee-content">
            <!-- Original Content -->
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <!-- Duplicate Content -->
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
            <p class="scrolling-text text-drop-shadow">#ALIVE</p>
        </div>
    </div>
</body>

"""
st.components.v1.html(html_string, height=360)

bucket_name = 'pictures'

response = supabase.storage().upload(bucket_name, file_path, image_data)

if "captured_image" not in st.session_state:
    st.session_state["captured_image"] = None
if "geocode_done" not in st.session_state:
    st.session_state["geocode_done"] = False

if st.session_state["captured_image"] is None:
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()

    take_picture = st.button("Take Picture")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to grab frame.")
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, use_column_width=True)

        if take_picture:
            st.session_state["captured_image"] = frame
            unique = "user_images\\" + str(uuid4()) + ".jpeg"
            st.session_state["unique_filename"] = unique
            cv2.imwrite(unique, frame)
            cap.release()
            break

if st.session_state["captured_image"] is not None and not st.session_state["geocode_done"]:
    address = st.text_input("Enter Your Address (include city, no zipcode, no commas)", placeholder="Enter an Address or a Location Name", key="address")
    name = st.text_input("Enter Your Name", placeholder="Enter Your Name", key="name")
    if address and name:
        st.write("Entered address:", address)
        st.write("Entered name:", name)

        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.geocode(address)

        if location:
            st.write("Latitude:", location.latitude)
            st.write("Longitude:", location.longitude)

            unique_filename = st.session_state.get("unique_filename")

            response = supabase.table("input_data").insert({
                "latitude": location.latitude,
                "longitude": location.longitude,
                "text_description": "No text yet",
                "address": address,
                "images": unique_filename,
                "name": name
            }).execute()
            
            with open(unique_filename, 'rb') as image_file:
                image_data = image_file.read()
            
            response2 = supabase.storage().upload(bucket_name, unique_filename, image_data)


            st.session_state["geocode_done"] = True
        else:
            st.write("Location not found. Please enter a valid address.")

            


