import streamlit as st
import os
from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

st.set_page_config(
    page_title="Photo Thread",
    page_icon="🧵",
    layout="wide"
)

st.title("Your Community Photo Thread 🧵")

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


response = supabase.table("input_data").select("*", count="exact").execute()
st.session_state["captured_image"] = None
st.session_state["geocode_done"] = False



user_data = supabase.table("input_data").select("images", "text_description", "address", "time_stamp").execute().data

for user in user_data:
    with st.container(border=True):

        filename = user["images"]
        caption_data = f"{user['address']} | {user['time_stamp']}"
        st.image(filename, caption=caption_data)