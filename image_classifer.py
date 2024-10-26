from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials

credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm/com",
    api_key = "",
    instance_id = "openshift",
)


client = APIClient(credentials)

client.models.list()