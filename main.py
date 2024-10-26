import streamlit as st
from dotenv import load_dotenv

import os
from supabase import create_client, Client

load_dotenv()
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")


url: str = os.environ.get(SUPABASE_URL)
key: str = os.environ.get(SUPABASE_KEY)
supabase: Client = create_client(url, key)

from streamlit_tailwind import st_tw

st.set_page_config(
    page_title="Main Page",
    page_icon="🌊",
	layout="wide"
)
st.sidebar.title("#ALIVE")
print("Hello World")
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://flood-api.open-meteo.com/v1/flood"
params = {
	"latitude": 59.91,
	"longitude": 10.75,
	"daily": "river_discharge"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_river_discharge = daily.Variables(0).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["river_discharge"] = daily_river_discharge


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



daily_dataframe = pd.DataFrame(data = daily_data)
print(daily_dataframe)
