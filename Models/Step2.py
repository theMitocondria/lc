
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
from Utils.Timer import timer_annotation;

load_dotenv()

chat = ChatGroq(
    temperature=0.5,
    model="llama3-70b-8192"
)


system = """
You are an efficient plagarism checker who identify the amount of code similarity according to data structures used in it and how they have been used with different variables and functions.
You follow these rules to do your task.

1. If two variables, data structures or functions are doing same work, you dont need to check their variable names, this means if you find two variables doing same contribution in the code to generate output you consider both of them in different codes to be same.
2. You cannot manipulate the code flow or any changes are not allowed.
3. You do not alter the similarity score on the basis of variable-name differences in the codes.
4. You do not alter the similarity score on the basis of spacing, indentation, and parentheses placement differences between the codes.
5. You understand that both the codes are solving same problem and hence not judge on the basis of resultant output of both

You are bold in nature hence different codes are given significantly low similarity % and vice versa.
Whenever anyone gives you two codes, you output similarity % of both the codes that are Code 1 and Code 2.

You give the similarity scores as valid json format i.e. {{"score":"floating point value of score only"}} and not write anything else outside this json.
Output should be a floating point value of similarity score only in the range of 0 to 1.
"""

human = "Code 1: \n```\n{code1}\n``` \n\nCode 2: \n```\n{code2}\n```"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

@timer_annotation
def Step2(code1 , code2):
    return chain.invoke({"code1": code1, "code2": code2}).content