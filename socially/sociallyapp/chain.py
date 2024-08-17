import openai
import os
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import json
load_dotenv()
openai_key = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = openai_key

post_template = """You are expert post writer for a social media platform. You are provided with a post text from a user. 
Your task is to improve the post and suggest a improved post to user. 
Instructions to follow :
1. Add emojis if required. 
2. Avoid to add hashtags. 


{postData}
{format_instructions}"""

response_schemas = [ ResponseSchema(name="improvedPost", description="Improves Post") ]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
print(format_instructions)
prompt_template=PromptTemplate(input_variables=['postData'],template=post_template,partial_variables={"format_instructions": format_instructions},)
#openAI can also be used here
post_llm=ChatOpenAI(temperature=0.4,model_name="gpt-3.5-turbo")
        
def chainResponse(postData : str):
    try:
        print(prompt_template)
        post_chain=LLMChain(llm=post_llm,prompt=prompt_template,verbose=True)
        chain_response =  post_chain({"postData":postData})
        data = chain_response['text']
        response = output_parser.parse(data)
        return response['improvedPost']        
    except Exception as e:
        print(f"Error in chainResponse: {e}")
        return {'error': 'Internal server error'}
    
print(chainResponse("Its raining today"))


