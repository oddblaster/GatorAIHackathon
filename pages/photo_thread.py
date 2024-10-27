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


response = supabase.table("input_data").select("*", count="exact").execute()
st.session_state["captured_image"] = None
st.session_state["geocode_done"] = False



user_data = supabase.table("input_data").select("images", "text_description", "address", "time_stamp").execute().data

for user in user_data:
    with st.container(border=True):

        filename = user["images"]
        caption_data = f"{user['time_stamp']} | {user['address']} | {user['text_description']}"
        st.image(filename, caption=caption_data)