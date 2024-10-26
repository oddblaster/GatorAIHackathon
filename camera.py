
import streamlit as st
import cv2
import pyaudio
import wave
import time

st.set_page_config(
    page_title="Recorder",
    page_icon="📹",
    
)

#Access the Camera
cap = cv2.VideoCapture(0)

while True:
    
    #Frame is the image itself a numpy, ret returns whether the camera works properly
    ret, frame = cap.read()
    
    #Shows the Frame
    cv2.imshow('frame', frame)
    
    #When button is pressed break the loop
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()




st.write("This is a test")

st.title()