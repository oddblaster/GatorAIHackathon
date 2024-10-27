import streamlit as st
from supabase import Client, create_client
import os 
from dotenv import load_dotenv

load_dotenv()

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


messages = st.container(height=500)





def get_responses():
    response = supabase.table("chat").select("*").execute()

    for row in response.data:
        messages.chat_message("human").write(row["message"])
            
if prompt := st.chat_input("Say something"):
    response = (
    supabase.table("chat")
    .insert({ "message" : prompt})
    .execute()
    )
    get_responses()