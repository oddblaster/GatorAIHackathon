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
CLOUD_API_KEY= os.getenv("CLOUD_API_KEY")
st.session_state["captured_image"] = None
st.session_state["geocode_done"] = False

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

st.set_page_config(
	layout="wide"
)

st.markdown(
    """
    <style>
    /* Set the main background to dark mode */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }

    /* Make sidebar background gray and set text to white */
    [data-testid="stSidebar"] {
        background-color: #333333;
    }

    /* Set sidebar text to white */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Make the top bar gray with white text */
    header, .css-18ni7ap {
        background-color: #333333 !important;
        color: #ffffff !important;
    }

    /* Customize primary Streamlit elements for dark mode */
    .css-1cpxqw2, .css-1v3fvcr, .css-hxt7ib, .css-1q8dd3e {
        background-color: #444444;
        color: #ffffff !important;
    }

    /* Set link colors to light gray for visibility */
    a {
        color: #9aa0a6;
    }

    /* Adjust buttons and inputs to match dark mode */
    button, input, textarea, select {
        background-color: #555555;
        color: #ffffff;
        border: 1px solid #666666;
    }
    </style>
    """,
    unsafe_allow_html=True
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


row = supabase.table("input_data").select("*").order("time_stamp", desc=True).limit(1).execute().data[0]

image_path = row["images"]
img = Image.open(image_path)
buffered = io.BytesIO()
img.save(buffered, format="JPEG")  # Save the image to the BytesIO object
encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Encode to Base64



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
st.image(image_path)

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
result = data['choices'][0]['message']['content']
st.write(result)








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
    GenParams.MAX_NEW_TOKENS: 4096,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.TEMPERATURE: 0.5,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1
}

project_id = os.environ["PROJECT_ID"]
print([model.name for model in ModelTypes])
st.write("Instructions")
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
    input_variables=["result"], 
    template='''
    Context:
    {result}
    
    Prompt:
    Measure the severity of the disaster on a scale from 1 to 100. With 1 being minimal damage,
    and 100 being the most damage a natural disaster has ever done. Respond ONLY as an integer.
    RETURN only the integer and nothing else.
     '''
)
disaster_response = PromptTemplate(
    input_variables=["result"],
    template='''
    context:
        {result}
    prompt:
    
    Objective: Develop a comprehensive action plan to effectively respond to the current natural disaster situation.

Step 1: Situation Assessment
1.1 Gather Information
Review real-time data from weather stations, satellites, and local reports.
Understand the scale and type of disaster (e.g., flood, earthquake, hurricane).
Identify the affected areas and magnitude of impact.
1.2 Conduct Field Assessments
Deploy drones or reconnaissance teams to survey and map hard-hit areas.
Assess on-ground conditions such as road accessibility, building damage, and infrastructure failure.
Use initial assessments to prioritize regions based on severity and urgency.
Step 2: Resource Mobilization
2.1 Inventory Resources
Compile a list of available resources: emergency personnel, vehicles, medical supplies, food and water, and shelters.
Identify additional resources that may be required and potential sources (government stockpiles, NGO supplies, international aid).
2.2 Allocate Resources
Develop a deployment strategy for rapid distribution based on priority zones.
Establish a centralized command center to coordinate resource allocation and manage real-time updates.
Prepare logistical plans for transportation, taking into account damaged infrastructure and accessibility issues.
Step 3: Communication Plan
3.1 Internal Communication
Set up a secure and reliable communication network among teams.
Regularly brief all teams on situational updates and strategic changes.
3.2 External Communication
Establish communication lines with local authorities, emergency services, and community leaders.
Utilize multi-channel communication strategies (social media, SMS alerts, radio broadcasts) to inform and instruct the public.
Step 4: Rescue and Relief Operations
4.1 Search and Rescue
Mobilize search and rescue teams to the most critical areas first.
Ensure teams are equipped with necessary gear such as medical kits, extraction tools, and communication devices.
Coordinate with local volunteers and international aid workers.
4.2 Provide Immediate Relief
Set up emergency shelters in safe locations with adequate facilities.
Ensure a continuous supply of basic needs: food, clean water, medical care, and sanitation.
Create a system for registering evacuees to track and reunite families.
Step 5: Restoration and Rehabilitation
5.1 Infrastructure Restoration
Work alongside engineering teams to begin immediate repair of essential infrastructure (roads, bridges, utilities).
Develop a long-term plan for rebuilding damaged buildings and homes.
5.2 Community Support
Offer psychological counseling and social support to affected residents.
Coordinate with health services to set up temporary clinics and extend medical care.
Implement educational programs to help people resume normal life activities.
Step 6: Review and Adaptation
6.1 Post-Operation Analysis
Conduct debriefings to evaluate the effectiveness of response efforts.
Collect feedback from field teams and affected communities.
6.2 Improve Future Preparedness
Identify areas of improvement and update disaster response protocols.
Conduct training and simulations based on lessons learned to enhance preparedness for future incidents.
Invest in infrastructure and technology to mitigate the impact of similar disasters.
This structured plan ensures a detailed and organized approach to responding to natural disasters, enhancing the effectiveness and efficiency of relief and recovery efforts.
    ''',
)


prompt_to_flan_ul2 = LLMChain(llm=llama, prompt=disaster_identification, output_key='severity')
flan_to_t5 = LLMChain(llm=flan_t5_llm, prompt=disaster_response, output_key='procedures')


qa = SequentialChain(chains=[prompt_to_flan_ul2, flan_to_t5], input_variables=["result"], output_variables=['severity', 'procedures'], verbose=True)

st.write(qa.invoke({"result": "result"}))

