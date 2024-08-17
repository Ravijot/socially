post_template = """You are expert post writer for a social media platform. You are provided with a post text from a user. 
# Your task is to improve the post and adding emojis if required. Avoid to add hashtags. {postData} """

# prompt_template=PromptTemplate(input_variables=['postData'],template=post_template)

# post_llm=OpenAI(openai_api_key=openai_key,temperature=0.4,model_name="gpt-3.5-turbo")

# post_chain=LLMChain(llm=post_llm,prompt=prompt_template,output_key="post",verbose=True)

# chain_response =  post_chain({"postData":"Its raining today"})
# print(chain_response['post'])