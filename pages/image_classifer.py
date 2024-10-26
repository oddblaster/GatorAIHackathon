from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
#from project_lib import Project
import streamlit
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64

load_dotenv()
IBM_API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")

credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                   api_key = "zGWBN0kyqZxsOc1wzsMDMqqO5r9Da49rTRwsBQYqt_jS",
                   
                  )

client = APIClient(credentials)

client.foundation_models.TextModels.show()

model = ModelInference(
    model_id="meta-llama/llama-3-2-90b-vision-instruct",
    decoding_method="greedy",
    repetition_penalty=1,
    api_client=client,
    project_id=PROJECT_ID,
    params={
        "max_new_tokens": 900
    }
)

# image_path = 'path/to/your/image.png'  # Specify the path to your image
# image = Image.open(image_path)
# open(image_path)

# Convert the image to bytes
# buffered = io.BytesIO()
# image.save(buffered, format="png")  # Change format if necessary
# img_bytes = buffered.getvalue()



prompt = 'However far is Paris from Bangalore'
print(model.generate(prompt))
print(model.generate_text(prompt))

# project = Project(project_id='b276164c1db74b33b706f91e9779fc4d', project_access_token='p-2+8miwtmlsF4C9FqhnpuYhwQ==;ud9WgqJXD3pkdc1/YW4+Vg==:p+Xj1FHPnJdgFXkxuDkqhjHcPMG2AiLKh0LV1vyofyOAx97uNzgDjDSE64Qb9F0LwBl7Fg6aRPPS5WwrMdZnogeYw901yPxxHQ==')
# pc = project.project_context

# credentials = Credentials(
#     url = "https://us-south.ml.cloud.ibm/com",
#     api_key = IBM_API_KEY,
#     instance_id = "openshift",
# )
