
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# import json
# from dotenv import load_dotenv
# from Utils.Timer import timer_annotation;

# load_dotenv()

# chat = ChatGroq(
#     temperature=0.5,
#     model="llama3-70b-8192"
# )


# system = """
# You are an efficient plagarism checker who identify the amount of code similarity according to data structures used in it and how they have been used with different variables and functions.
# You follow these rules to do your task.

# 1. If two variables, data structures or functions are doing same work, you dont need to check their variable names, this means if you find two variables doing same contribution in the code to generate output you consider both of them in different codes to be same.
# 2. You cannot manipulate the code flow or any changes are not allowed.
# 3. You do not alter the similarity score on the basis of variable-name differences in the codes.
# 4. You do not alter the similarity score on the basis of spacing, indentation, and parentheses placement differences between the codes.
# 5. You understand that both the codes are solving same problem and hence not judge on the basis of resultant output of both

# You are bold in nature hence different codes are given significantly low similarity % and vice versa.
# Whenever anyone gives you two codes, you output similarity % of both the codes that are Code 1 and Code 2.

# You give the similarity scores as valid json format i.e. {{"score":"floating point value of score only"}} and not write anything else outside this json.
# Output should be a floating point value of similarity score only in the range of 0 to 1.
# """

# human = "Code 1: \n```\n{code1}\n``` \n\nCode 2: \n```\n{code2}\n```"
# prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# chain = prompt | chat

# @timer_annotation
# def Step2(code1 , code2):
#     return chain.invoke({"code1": code1, "code2": code2}).content


from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
from itertools import cycle
import os
from Utils.Timer import timer_annotation

load_dotenv()

# Load API keys from .env file
api_keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(1, 6)]
api_keys_cycle = cycle(api_keys)

# Function to create a ChatGroq instance with a given API key
def create_chat_instance(api_key):
    print(api_key)
    return ChatGroq(
        temperature=0.5,
        model="llama3-70b-8192",
        api_key=api_key
    )

system = """
You are an efficient plagiarism checker who identifies the amount of code similarity according to data structures used in it and how they have been used with different variables and functions.
You follow these rules to do your task.

1. If two variables, data structures, or functions are doing the same work, you don't need to check their variable names. This means if you find two variables doing the same contribution in the code to generate output, you consider both of them in different codes to be the same.
2. You cannot manipulate the code flow or any changes are not allowed.
3. You do not alter the similarity score on the basis of variable-name differences in the codes.
4. You do not alter the similarity score on the basis of spacing, indentation, and parentheses placement differences between the codes.
5. You understand that both the codes are solving the same problem and hence do not judge on the basis of the resultant output of both.

You are bold in nature hence different codes are given significantly low similarity % and vice versa.
Whenever anyone gives you two codes, you output similarity % of both the codes that are Code 1 and Code 2.

You give the similarity scores as valid JSON format i.e. {{"score":"floating point value of score only"}} and not write anything else outside this JSON.
Output should be a floating point value of similarity score only in the range of 0 to 1.
"""

human = "Code 1: \n```\n{code1}\n``` \n\nCode 2: \n```\n{code2}\n```"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# Initialize the first ChatGroq instance and set the request counter
current_api_key = next(api_keys_cycle)
chat = create_chat_instance(current_api_key)
request_counter = 0
max_requests_per_key = 4

chain = prompt | chat

@timer_annotation
def Step2(code1, code2):
    global chat, request_counter, current_api_key
    # Increment the request counter
    request_counter += 1
    
    # Check if we've reached the max requests per key
    if request_counter > max_requests_per_key:
        # Reset the counter and rotate the API key
        request_counter = 1
        current_api_key = next(api_keys_cycle)
        chat = create_chat_instance(current_api_key)
    
    return chain.invoke({"code1": code1, "code2": code2}).content
