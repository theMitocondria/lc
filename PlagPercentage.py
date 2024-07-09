import json
from modal import checkPlagPercentage
# Load JSON data from 1.json file
with open('responses1.json', 'r') as file:
    data = json.load(file)

st = set()

for curr in range(0, 6) : 
    st.add((checkPlagPercentage(data[curr]['code']), data[curr]['rank']))

print(st)