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

st.markdown(
    """
    <style>
    /* Set the main background to dark mode */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }

    /* Make sidebar background gray and set text to white */
    [data-testid="stSidebar"] {
        background-color: #333333;
    }

    /* Set sidebar text to white */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Make the top bar gray with white text */
    header, .css-18ni7ap {
        background-color: #333333 !important;
        color: #ffffff !important;
    }

    /* Customize primary Streamlit elements for dark mode */
    .css-1cpxqw2, .css-1v3fvcr, .css-hxt7ib, .css-1q8dd3e {
        background-color: #444444;
        color: #ffffff !important;
    }

    /* Set link colors to light gray for visibility */
    a {
        color: #9aa0a6;
    }

    /* Adjust buttons and inputs to match dark mode */
    button, input, textarea, select {
        background-color: #555555;
        color: #ffffff;
        border: 1px solid #666666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

        .marquee-container {
            overflow: hidden;
            width: 100%;
            display: flex;
            align-items: center;
        }

        .marquee-content {
            display: flex;
            /* Ensure the content width adjusts based on its content */
            width: max-content;
            animation: scroll-left 15s linear infinite;
        }

        /* Prevent items from shrinking when overflowing */
        .marquee-content > * {
            flex-shrink: 0;
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
    <div class="marquee-container">
        <div class="marquee-content">
            <!-- Original Content -->
            <div class="marquee-group">
                <p class="text-drop-shadow">#ALIVE</p>
                <p class="text-drop-shadow">#ALIVE</p>
                <p class="text-drop-shadow">#ALIVE</p>
                <p class="text-drop-shadow">#ALIVE</p>
            </div>
            <!-- Duplicate Content -->
            <div class="marquee-group">
                <p class="text-drop-shadow">#ALIVE</p>
                <p class="text-drop-shadow">#ALIVE</p>
                <p class="text-drop-shadow">#ALIVE</p>
                <p class="text-drop-shadow">#ALIVE</p>
            </div>
        </div>
    </div>
</body>
"""
mission_statement = """
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
    <div class="marquee-container h-full bg-transparent">
    <p class="scrolling-text text-drop-shadow text-7xl mb-6">#HOW WERE YOU AFFECTED?</p>
    </div>
</body>
"""

st.components.v1.html(html_string, height=150)
st.components.v1.html(mission_statement, height=100)
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
            
    from ibm_watsonx_ai import APIClient
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    #from project_lib import Project
    import streamlit as st
    import os
    from dotenv import load_dotenv
    from PIL import Image
    from supabase import Client, create_client
    import io
    import base64
    import requests

    load_dotenv()
    IBM_API_KEY = os.getenv("IBM_API_KEY")
    PROJECT_ID = os.getenv("PROJECT_ID")
    CLOUD_API_KEY= os.getenv("CLOUD_API_KEY")
    st.session_state["captured_image"] = None
    st.session_state["geocode_done"] = False

    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    st.set_page_config(
        layout="wide"
    )

    def generate_access_token(CLOUD_API_KEY, IAM_URL):
        headers={}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Accept"] = "application/json"
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": IBM_API_KEY,
            "response_type": "cloud_iam"
        }
        response = requests.post(IAM_URL, data=data, headers=headers)
        json_data = response.json()
        iam_access_token = json_data['access_token']
        return iam_access_token

    IAM_URL = "https://iam.cloud.ibm.com/identity/token"
    access_token = generate_access_token(CLOUD_API_KEY, IAM_URL)

    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29",
        "project_id": PROJECT_ID,
        "bearer_token": f"Bearer {access_token}"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": credentials.get("bearer_token")
    }


    row = supabase.table("input_data").select("*").order("time_stamp", desc=True).limit(1).execute()


    image_path = row["images"]
    img = Image.open(image_path)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")  # Save the image to the BytesIO object
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Encode to Base64

    # print('saved_image.png')


    def augment_api_request_body(user_query, image):
        body = {
                "messages": [{"role":"user","content":[{"type":"text","text": '''
                Conduct an exhaustive analysis of the attached image with a focus on several critical elements to understand the full scope and context of the disaster. Your analysis should be highly detailed and structured as follows:

                Weather Conditions:
                    Current Weather: Document the present weather conditions, including temperature, humidity, wind speed, visibility, and precipitation. Note any severe weather warnings in effect.
                    Meteorological Impact: Examine how the weather may have exacerbated the disaster, including the role of wind in spreading debris, or how precipitation might have affected flooding or landslides.
                Damage Assessment:
                    Structural Damage: Provide a detailed evaluation of damage to buildings, bridges, roads, and other infrastructure. Identify which structures are partially or completely destroyed.
                    Resource Impairment: Determine the extent of damage to utilities such as power lines, water supply, sewage systems, and telecommunications.
                Surrounding Environment:
                    Natural Features:
                        Topography: Detail the terrain characteristics (e.g., flat, hilly, mountainous) and any significant geographical features (e.g., rivers, lakes, coastal areas) that might influence the disaster dynamics.
                Built Environment:
                    Urban Layout: Describe the layout of urban areas, including zoning details such as residential, commercial, or industrial regions.
                Infrastructure: Detail the condition and relevance of roads, bridges, railways, and public transportation networks, noting any observed damage or impediments to use.
    ''' + user_query},
                    {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{image}"}}]}],
                "project_id": credentials.get("project_id"),
                "model_id": "meta-llama/llama-3-2-90b-vision-instruct",
                "decoding_method": "greedy",
                "repetition_penalty": 1,
                "max_tokens": 8000
        }
        return body
    st.image("image.jpeg")

    image = encoded_image
    user_query = "What is happening in this image?"
    request_body = augment_api_request_body(user_query, image)
    response = requests.post(
        credentials.get("url"),
        headers=headers,
        json=request_body
        )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    data = response.json()
    result = data['choices'][0]['message']['content']
    st.write(result)









