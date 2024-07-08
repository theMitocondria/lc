from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
from Utils.Timer import timer_annotation;

load_dotenv()

chat = ChatGroq(
    temperature=0,
    model="gemma2-9b-it"
)

system = """
You are efficient code optimizer.
You operate in the following way.

1) You remove all the comments from the codes.
2) You unnecessary  variables, loops, and function calls which are not affecting the results or return values.

You give the processed codes as output in the valid json format i.e. {{"processedCode":"output code after processing"}} and not write anything else outside this json.

"""

human = "Code: \n{code}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain1 = prompt | chat

def processcode(txt):
    if not txt.startswith("{"):
        txt = txt[7:-3].strip()

    out1 = json.loads(txt)
    processed1 = out1["processedCode"]
    return processed1

@timer_annotation
def Step1(code1) :

    out1 = chain1.invoke({"code": code1}).content
    # print(out1)

    processed1 = processcode(out1)
    return processed1

