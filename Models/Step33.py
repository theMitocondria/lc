
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
Task:

Your task is to analyze two code snippets and determine the likelihood of plagiarism, returning a percentage value between 0 (no plagiarism) and 100 (complete plagiarism).

Objective:

Code Cleaning:

Remove comments, whitespace, and redundant code constructs that do not affect the final output.
Standardize variable and data structure names for a consistent comparison.
Eliminate template code commonly reused in competitive programming and focus on the core logic.
Cross-Language Plagiarism Detection:

Translate and compare logic across different programming languages (e.g., C++ to Java, Python).
Identify and flag cases where code has been translated to avoid plagiarism detection.
Functionality and Logic Focus:

Focus on the actual logic and unique parts of the code rather than common structures like segment tree templates.
Analyze how standard algorithms are applied rather than the presence of the algorithms themselves.
N-grams Analysis:

Utilize character n-grams and token n-grams to capture low-level syntax and high-level code structures.
Break the code into overlapping n-grams of varying sizes and compare their frequencies to detect similarities.

Bag-of-Words (BoW):

Represent code snippets as a bag of tokens and compare the frequency of each token.
Identify high similarity in BoW representations to suggest potential plagiarism.
TF-IDF Analysis:

Use TF-IDF to evaluate the significance of terms within code snippets.
High TF-IDF scores for unique terms indicate distinguishing features of the code.
Example: Common terms like 'if,' 'else,' and 'int' have lower scores, while unique variable names have higher scores.
Structural Analysis:

Compare Abstract Syntax Trees (ASTs) to evaluate structural similarity.
Analyze Control Flow Graphs (CFGs) and function call graphs for pattern similarities.
Example: Identical or highly similar ASTs indicate structural plagiarism.
Semantic Analysis:

Use embeddings from models like CodeBERT or GraphCodeBERT to capture the semantic meaning of code.
Generate vector representations of code snippets and compare their similarities.
Example: Similar code embeddings indicate semantic plagiarism.
Metadata Analysis:

Evaluate the submission history of authors to identify patterns of plagiarism.
Consider the time difference between submissions as a potential indicator of copying.
Example: Short time differences between similar submissions suggest possible plagiarism.
You give the similarity scores as valid json format i.e. {{"score": "floating point value of score only"}} and not write anything else outside this json.


"""


human = "Code 1: \n```\n{code1}\n``` \n\nCode 2: \n```\n{code2}\n```"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

@timer_annotation
def Step33(code1 , code2):
    return chain.invoke({"code1": code1, "code2": code2}).content

