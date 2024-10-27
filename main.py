import streamlit as st
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

st.set_page_config(
    page_title="Main Page",
    page_icon="🌊",
	layout="wide"
)
st.sidebar.title("#ALIVE")


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
