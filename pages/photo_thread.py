import streamlit as st
import os
from supabase import Client, create_client
from dotenv import load_dotenv
from PIL import Image
import io
import base64

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
        new_file = user['images']
        try:
            response3 = supabase.storage.from_("pictures").download(new_file)
            image = response3
            img = Image.open(io.BytesIO(image))
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG") 
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Encode to Base64d image.jpeg
            encoded_image_with_prefix = f"data:image/jpeg;base64,{encoded_image}"
            caption = f'{user["time_stamp"]} | {user["address"]}'
            st.image(encoded_image_with_prefix, caption=caption)
            
            
        except Exception:
            print("no image")