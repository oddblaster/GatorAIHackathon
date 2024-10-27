import streamlit as st
import os
from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

response = supabase.table("input_data").select("text_description").order("timestamp", desc=True).limit(1).execute()
st.write(response)

st.title("Survivors Map")

st.map()