
import streamlit as st
import cv2
import pyaudio
import wave
import time

st.set_page_config(
    page_title="Recorder",
    page_icon="📹",
    
    
)
st.title("Hello World")

#Access the Camera
cap = cv2.VideoCapture(0)

frame_placeholder = st.empty()
while True:
    
    #Frame is the image itself a numpy, ret returns whether the camera works properly
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))
    
     
    #Shows the Frame
    frame_placeholder.image(frame, channels="BGR")
    
    #When button is pressed break the loop
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()




st.write("This is a test")

st.title()