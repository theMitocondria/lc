
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

Input:

Code Snippet 1: The first code snippet (suspected of plagiarism).
Code Snippet 2: The second code snippet (reference code).
Programming Language: The language of the code snippets (e.g., Python, Java, C++).
Metadata (Optional): Any relevant metadata, such as author information or submission timestamps.
Output:

A plagiarism score between 0 and 100, indicating the percentage of similarity between the code snippets.

Key Considerations:

Code Cleaning:

Remove comments, unnecessary whitespace, and unused variables or functions.
Standardize variable and data structure names to normalize differences in naming conventions.
Handle different programming languages effectively (e.g., normalize syntax variations).
Feature Extraction:

Textual Features:
Extract n-grams (character and token) of various lengths to capture low-level and higher-level code patterns.
Create Bag-of-Words (BoW) representations to capture word frequencies.
Compute TF-IDF scores to weigh the importance of terms based on their frequency and rarity.
Structural Features:
Analyze abstract syntax trees (ASTs) to compare the structure and organization of code.
Examine control flow graphs (CFGs) to compare the logic and execution paths.
Look for similarities in function call graphs to identify similar patterns of function usage.
Semantic Features:
Utilize pre-trained code embeddings (like CodeBERT or GraphCodeBERT) to capture the semantic meaning of the code.
Metadata Features (Optional):
Consider author history and submission timestamps to identify potential patterns of plagiarism.
Similarity Calculation:

Use appropriate similarity metrics (e.g., cosine similarity) to compare the extracted features between the two code snippets.
Weight the importance of different features based on their relevance to plagiarism detection (e.g., structural features may be more important than textual features in some cases).
Threshold Determination:

Set a plagiarism threshold (e.g., 80%) based on the analysis of your training data and the specific requirements of your coding contest.
Ensure that the threshold strikes a balance between detecting actual plagiarism and minimizing false positives.
Logic-Focused Analysis:

Prioritize the analysis of the core logic and algorithm used in the code snippets.
Distinguish between genuine plagiarism and the use of common patterns or templates (e.g., segment tree implementation) that might be necessary for solving the problem.
Example Output:

Plagiarism Score: 95% (High likelihood of plagiarism)
Additional Notes:

False Positives: Be mindful of the risk of false positives and prioritize accuracy over sensitivity.
Evolving Tactics: Be prepared to adapt your model over time to counter new plagiarism techniques.
Feedback Loop: Consider incorporating feedback mechanisms (e.g., human review) to continuously improve the model's accuracy.

You give the similarity scores as valid json format i.e. {{"score":"floating point value of score only"}} and not write anything else outside this json.
"""

human = "Code 1: \n```\n{code1}\n``` \n\nCode 2: \n```\n{code2}\n```"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

@timer_annotation
def Step22(code1 , code2):
    return chain.invoke({"code1": code1, "code2": code2}).content