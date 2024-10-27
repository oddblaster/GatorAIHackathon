import streamlit as st
import os
import numpy as np
import pandas as pd
from supabase import Client, create_client
from dotenv import load_dotenv


st.markdown(
    """
    <style>
    /* Set the main background to dark mode */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

response = supabase.table("input_data").select("*", count="exact").execute()
st.session_state["captured_image"] = None
st.session_state["geocode_done"] = False


user_lat = supabase.table("input_data").select("latitude").execute().data
user_long = supabase.table("input_data").select("longitude").execute().data
severity = supabase.table("input_data").select("ranking").execute().data

if user_lat and user_long and severity:
  latitudes = [entry['latitude'] for entry in user_lat]
  longitudes = [entry['longitude'] for entry in user_long]
  severities = [entry['ranking'] for entry in severity]
  


st.title("Survivors Map")
df = pd.DataFrame(
  {
    "lat": latitudes,
    "lon": longitudes,
    "size": [100*entry for entry in severities]
  }
)

st.map(df, latitude="lat", longitude="lon", color="#FF00FF", size="size")
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
