from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
#from project_lib import Project
import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from supabase import Client, create_client
import io
import base64
import requests

load_dotenv()
IBM_API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
st.session_state["captured_image"] = None
st.session_state["geocode_done"] = False

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

st.set_page_config(
	layout="wide"
)

def generate_access_token(CLOUD_API_KEY, IAM_URL):
    headers={}
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Accept"] = "application/json"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": IBM_API_KEY,
        "response_type": "cloud_iam"
    }
    response = requests.post(IAM_URL, data=data, headers=headers)
    json_data = response.json()
    iam_access_token = json_data['access_token']
    return iam_access_token

IAM_URL = "https://iam.cloud.ibm.com/identity/token"
access_token = generate_access_token(CLOUD_API_KEY, IAM_URL)

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29",
    "project_id": PROJECT_ID,
    "bearer_token": f"Bearer {access_token}"
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": credentials.get("bearer_token")
}


row = supabase.table("input_data").select("*").order("time_stamp", desc=True).limit(1).execute()


image_path = row["images"]
img = Image.open(image_path)
buffered = io.BytesIO()
img.save(buffered, format="JPEG")  # Save the image to the BytesIO object
encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Encode to Base64

# print('saved_image.png')


def augment_api_request_body(user_query, image):
    body = {
            "messages": [{"role":"user","content":[{"type":"text","text": '''
            Conduct an exhaustive analysis of the attached image with a focus on several critical elements to understand the full scope and context of the disaster. Your analysis should be highly detailed and structured as follows:

            Weather Conditions:
                Current Weather: Document the present weather conditions, including temperature, humidity, wind speed, visibility, and precipitation. Note any severe weather warnings in effect.
                Meteorological Impact: Examine how the weather may have exacerbated the disaster, including the role of wind in spreading debris, or how precipitation might have affected flooding or landslides.
            Damage Assessment:
                Structural Damage: Provide a detailed evaluation of damage to buildings, bridges, roads, and other infrastructure. Identify which structures are partially or completely destroyed.
                Resource Impairment: Determine the extent of damage to utilities such as power lines, water supply, sewage systems, and telecommunications.
            Surrounding Environment:
                Natural Features:
                    Topography: Detail the terrain characteristics (e.g., flat, hilly, mountainous) and any significant geographical features (e.g., rivers, lakes, coastal areas) that might influence the disaster dynamics.
            Built Environment:
                Urban Layout: Describe the layout of urban areas, including zoning details such as residential, commercial, or industrial regions.
            Infrastructure: Detail the condition and relevance of roads, bridges, railways, and public transportation networks, noting any observed damage or impediments to use.
''' + user_query},
                {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{image}"}}]}],
            "project_id": credentials.get("project_id"),
            "model_id": "meta-llama/llama-3-2-90b-vision-instruct",
            "decoding_method": "greedy",
            "repetition_penalty": 1,
            "max_tokens": 8000
    }
    return body
st.image("saved.jpeg")

image = encoded_image
user_query = "What is happening in this image?"
request_body = augment_api_request_body(user_query, image)
response = requests.post(
    credentials.get("url"),
    headers=headers,
    json=request_body
    )
if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))
data = response.json()
st.write(data['choices'][0]['message']['content'])


import getpass
from ibm_watsonx_ai import Credentials
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_ibm import WatsonxLLM
import os



load_dotenv()
IBM_API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key=IBM_API_KEY,
)

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.SAMPLE.value,
    GenParams.MAX_NEW_TOKENS: 100,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.TEMPERATURE: 0.5,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1
}

project_id = os.environ["PROJECT_ID"]
print([model.name for model in ModelTypes])

model_id_1 = ModelTypes.LLAMA_3_70B_INSTRUCT.value
model_id_2 = ModelTypes.FLAN_T5_XXL.value

llama = WatsonxLLM(
    model_id=model_id_1,
    url=credentials["url"],
    apikey=credentials["apikey"],
    project_id=project_id,
    params=parameters
    )

flan_t5_llm = WatsonxLLM(
    model_id=model_id_2,
    url=credentials["url"],
    apikey=credentials["apikey"],
    project_id=project_id
    )

disaster_identification = PromptTemplate(
    input_variables=["disaster_analysis"], 
    template='''f: 
     '''
)
disaster_response = PromptTemplate(
    input_variables=["disaster_response"],
    template="Answer the following question: {question}",
)


prompt_to_flan_ul2 = LLMChain(llm=llama, prompt=disaster_identification, output_key='question')
flan_to_t5 = LLMChain(llm=flan_t5_llm, prompt=disaster_response, output_key='answer')
sample_payload = {
    "input_data": [
        {
            "fields": ["disaster_analysis"],
            "values": ["disaster_response   "]
        }
    ]
}


qa = SequentialChain(chains=[prompt_to_flan_ul2, flan_to_t5], input_variables=["disaster_analysis"], output_variables=['question', 'answer'], verbose=True)

qa.invoke({"disaster_analysis": "disaster_response"})

