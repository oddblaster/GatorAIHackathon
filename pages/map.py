import streamlit as st
import os
import numpy as np
import pandas as pd
from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

user_lat = supabase.table("input_data").select("latitude").order("timestamp", desc=True).limit(1).execute().data[0]
user_long = supabase.table("input_data").select("longitude").order("timestamp", desc=True).limit(1).execute().data[0]

st.write(user_lat)
st.write(user_long)

st.title("Survivors Map")
df = pd.DataFrame(
    {
        "lat": [user_lat['latitude']],
        "lon": [user_long['longitude']]

    }
)
st.write(df['lat'])
st.write(df['lon'])

st.map(df, latitude="lat", longitude="lon", color="#FF0000", size=50)
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
