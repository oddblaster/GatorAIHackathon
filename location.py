import socket
import geopy
import streamlit as st
import json
import dotenv
from dotenv import load_dotenv
import os 
load_dotenv()
IPAPI_KEY = os.getenv("IPAPI_API")

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
from requests import get

ip = get('https://api.ipify.org').text
st.write('My public IP address is: {}'.format(ip))

url = f'https://api.ipapi.com/api/{ip}?access_key={IPAPI_KEY}&fields=latitude,longitude'
response = get(url)
data = response.json()
parsed = json.dumps(data)

st.write(data)