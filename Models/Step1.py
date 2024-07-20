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
    api_key =os.getenv(f'GROQ_API_KEY_5')
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

# @timer_annotation
def Step1(code1) :

    out1 = chain1.invoke({"code": code1}).content
    processed1 = processcode(out1)
    return processed1

