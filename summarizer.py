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
    template='''{disaster}: 
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


qa = SequentialChain(chains=[prompt_to_flan_ul2, flan_to_t5], input_variables=["topic"], output_variables=['question', 'answer'], verbose=True)

qa.invoke({"disaster_analysis": "life"})
