from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
import os
from Utils.Timer import timer_annotation;

load_dotenv()

chat = ChatGroq(
    temperature=0,
    model="gemma2-9b-it",
    api_key =os.getenv(f'GROQ_API_KEY_1')
)

system = """
You are efficient code optimizer.
You operate in the following way.

1) You remove all the comments from the codes.
2) You unnecessary  variables, loops, and function calls which are not affecting the results or return values.

You give the processed codes as output in the valid string literal format i.e. "output code after processing" and not write anything else outside this string.
You always take care of  escaping the special characters properly in the ouput string of the code.
"""

human = "Code: \n{code}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain1 = prompt | chat

def processcode(txt):
    # print(txt[1:-1])

    return txt[1:-1]
    # txt = '%r'%txt
    
    # try:
    #     out1 = json.loads(txt)
    #     processed1 = out1["processedCode"]
    #     return processed1
    # except:
    #     out1 = json.loads(txt)
    #     processed1 = out1["processedCode"]
    #     return processed1

@timer_annotation
def Step1(code1) :

    out1 = chain1.invoke({"code": code1}).content
    # print(out1)

    processed1 = processcode(out1)
    return processed1


# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# import json
# from dotenv import load_dotenv
# import os
# from itertools import cycle
# from Utils.Timer import timer_annotation

# load_dotenv()

# # Load API keys from .env file
# api_keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 3)]
# api_keys_cycle = cycle(api_keys)

# # Function to create a ChatGroq instance with a given API key
# def create_chat_instance(api_key):
#     return ChatGroq(
#         temperature=0,
#         model="gemma2-9b-it",
#         api_key=api_key
#     )

# system = """
# You are an efficient code optimizer.
# You operate in the following way:
# 1) You remove all the comments from the codes.
# 2) You remove unnecessary variables, loops, and function calls which are not affecting the results or return values.
# You give the processed codes as output in the valid string literal format i.e. "output code after processing" and not write anything else outside this string.
# You always take care of escaping the special characters properly in the output string of the code.
# """

# human = "Code: \n{code}"
# prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# # Initialize the first ChatGroq instance and set the request counter
# current_api_key = next(api_keys_cycle)
# chat = create_chat_instance(current_api_key)
# request_counter = 0
# max_requests_per_key = 8

# chain1 = prompt | chat

# def process_code(txt):
#     return txt[1:-1]

# @timer_annotation
# def Step1(code1):
#     global chat, request_counter, current_api_key
#     # Increment the request counter
#     request_counter += 1
    
#     # Check if we've reached the max requests per key
#     if request_counter > max_requests_per_key:
#         # Reset the counter and rotate the API key
#         request_counter = 1
#         current_api_key = next(api_keys_cycle)
#         chat = create_chat_instance(current_api_key)

#     out1 = chain1.invoke({"code": code1}).content
#     processed1 = process_code(out1)
#     return processed1

