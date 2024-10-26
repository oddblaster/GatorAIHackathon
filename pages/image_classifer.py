from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from project_lib import Project
import streamlit


project = Project(project_id='YOUR_PROJECT_ID', project_access_token='YOUR_PROJECT_TOKEN')
pc = project.project_context

credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm/com",
    api_key = ,
    instance_id = "openshift",
)


client = APIClient(credentials)

client.models.list()