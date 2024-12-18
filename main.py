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

st.markdown(
    """
    <style>
    /* Create an animated gradient background */
    @keyframes gradient {
        0% { background-position: 0% 100%; }
        50% { background-position: 0% 140%; }
        100% { background-position: 0% 100%; }
    }

    .stApp {
        background: linear-gradient(0deg, #000000, #000000, #39FF14, #000000, #000000);
        background-size: 600% 600%;
        animation: gradient 12s ease infinite;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("#ALIVE")
st.session_state["captured_image"] = None
st.session_state["geocode_done"] = False

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
            animation: scroll-left 10s linear infinite;
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
    <p class="scrolling-text text-drop-shadow text-7xl mb-6">#MISSION STATEMENT</p>
    </div>
	<p class="scrolling-text text-drop-shadow text-2xl mb-20">Our mission is to empower communities and enhance disaster response efforts <br/> through a crowd-sourced incident tracking platform. <br/> By connecting people in crisis, we aim to improve situational awareness, <br/> streamline rescue operations, and ultimately save lives during natural disasters.</p>
	<p class="text-drop-shadow text-2xl">By: #Hemanshu Boppana</p>
	<p class="text-drop-shadow text-2xl">#Department of Statistics</p>
	<p class="text-drop-shadow text-2xl">#Eren Chang</p>
	<p class="text-drop-shadow text-2xl">#HWCOE</p>
	<p class="text-drop-shadow text-2xl">#Chuyang Zhang</p>
	<p class="text-drop-shadow text-2xl">#HWCOE</p>
	<p class="text-drop-shadow text-2xl">#Jack Gordon</p>
	<p class="text-drop-shadow text-2xl">#HWCOE</p>
	<p class="text-drop-shadow text-2xl">#Maggie Yan</p>
	<p class="text-drop-shadow text-2xl">#HWCOE</p>
</body>
"""
st.components.v1.html(html_string, height=196)
st.components.v1.html(mission_statement, height=400)