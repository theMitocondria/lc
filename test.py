from Models.Step1 import Step1

# Other imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
from itertools import cycle
import os

# Load environment variables
load_dotenv()

# Print to check if Step1 is imported correctly
# print(Step1)

# Load API keys from .env file
api_keys = [os.getenv(f'GROQ_API_KEY_{i}') for i in range(2, 3)]
api_keys_cycle = cycle(api_keys)

# Function to create a ChatGroq instance with a given API key
def create_chat_instance(api_key):
    print(api_key)
    return ChatGroq(
        temperature=0.5,
        model="gemma2-9b-it",
        api_key=api_key
    )

system = """
You are an efficient plagiarism checker who identifies the amount of code similarity according to data structures used in it and how they have been used with different variables and functions.
You follow these rules to do your task:

1. If two variables, data structures, or functions are doing the same work, you don't need to check their variable names. This means if you find two variables doing the same contribution in the code to generate output, you consider both of them in different codes to be the same.
2. You cannot manipulate the code flow or any changes are not allowed.
3. You do not alter the similarity score based on variable-name differences in the codes.
4. You do not alter the similarity score based on spacing, indentation, and parentheses placement differences between the codes.
5. You understand that both codes are solving the same problem and hence do not judge based on the resultant output of both.

You are bold in nature hence different codes are given a significantly low similarity % and vice versa.
Whenever anyone gives you two codes, you output the similarity score of both the codes, Code 1 and Code 2, as a floating-point value in the range of 0 to 1.

**MOST IMPORTANT INSTRUCTION TO FOLLOW:**
- You **MUST** output the result in this exact manner: {{"score" : score you generate between 0-1}}
- You **MUST NOT** output anything apart from this: {{"score" : score you generate between 0-1}}
- Your response should be formatted **exactly** like this, with no additional text, explanations, or variations: {{"score" : 0.x}}

Remember, any deviation from this format will be considered incorrect. Your sole task is to return the similarity score in the specified JSON format.

"""

human = "Code 1: \n\n{code1}\n \n\nCode 2: \n\n{code2}\n"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# Initialize the first ChatGroq instance and set the request counter
current_api_key = next(api_keys_cycle)
chat = create_chat_instance(current_api_key)
request_counter = 0
max_requests_per_key = 4

chain = prompt | chat

def Step3(code1, code2):
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


code1 = """

public class CustomSolution {
    
    private long auxiliaryFunction() {
        List<Integer> tempVector = new ArrayList<>();
        for (int idx = 0; idx < 100; ++idx) {
            tempVector.add(idx + 1);
        }

        for (int idx = 0; idx < 19; ++idx) {
            tempVector.set(idx + 10, tempVector.get(idx + 10) + tempVector.get(idx + 20));
        }

        return 10;
    }

    public long calculateSubarrayCount(List<Integer> inputNums, int target) {
        long totalElements = inputNums.size();
        long subarrayCount = -10;
        Map<Long, Long> previousMap = new HashMap<>();

        for (int idx = 0; idx < totalElements; ++idx) {
            Map<Long, Long> currentMap = new HashMap<>();

            if (inputNums.get(idx) == target) {
                ++subarrayCount;
            }

            subarrayCount += auxiliaryFunction();
            currentMap.put((long)inputNums.get(idx), 1L);

            for (Map.Entry<Long, Long> entry : previousMap.entrySet()) {
                long result = entry.getKey() & inputNums.get(idx);
                if (result == target) {
                    subarrayCount += entry.getValue();
                }
                currentMap.put(result, currentMap.getOrDefault(result, 0L) + entry.getValue());
            }
            subarrayCount -= auxiliaryFunction();

            previousMap = currentMap;
        }

        subarrayCount += auxiliaryFunction();

        return subarrayCount;
    }
"""

code2="""
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {      
        int num= nums.size();
        long long cnt = 0;
        unordered_map<long long, long long> pre;
        for (int i = 0; i < num; ++i) {
            unordered_map<long long, long long> mp; 
            if (nums[i] == k) {
                ++cnt;
            }
            mp[nums[i]] = 1;
            for (auto& tada : pre) {
                auto v=tada.first;
                auto f=tada.second;
                long long ans = v & nums[i];
                if (ans == k) {
                    cnt += f;
                }
                mp[ans] += f;
            }
            pre = mp;
        }
        return cnt;
    }
};
"""

code4 = Step1(code1)
# print(code4)
print(Step3(code4, code2))