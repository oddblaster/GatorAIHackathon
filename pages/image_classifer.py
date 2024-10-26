from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
#from project_lib import Project
import streamlit
import os
from dotenv import load_dotenv

load_dotenv()
IBM_API_KEY = os.getenv("IBM_API_KEY")


credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                   api_key = "",
                  )

api_client = APIClient(credentials)

api_client.foundation_models.TextModels.show()

# project = Project(project_id='b276164c1db74b33b706f91e9779fc4d', project_access_token='p-2+8miwtmlsF4C9FqhnpuYhwQ==;ud9WgqJXD3pkdc1/YW4+Vg==:p+Xj1FHPnJdgFXkxuDkqhjHcPMG2AiLKh0LV1vyofyOAx97uNzgDjDSE64Qb9F0LwBl7Fg6aRPPS5WwrMdZnogeYw901yPxxHQ==')
# pc = project.project_context

# credentials = Credentials(
#     url = "https://us-south.ml.cloud.ibm/com",
#     api_key = IBM_API_KEY,
#     instance_id = "openshift",
# )


client = APIClient(credentials)

client.models.list()