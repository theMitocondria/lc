from Models.Step1 import Step1;
from Models.Step2 import Step2;
# from Utils.Timer import timer_annotation;


code4 = """
class Solution {
public:
     long long countSubarrays(vector<int>& nums, int k) {
        int n = nums.size();
        long long count = 0;
        
        unordered_map<long long, long long> prevResults;

        for (int i = 0; i < n; ++i) {
            unordered_map<long long, long long> currResults; 

            if (nums[i] == k) {
                ++count;
            }
            currResults[nums[i]] = 1;

            for (auto& [val, freq] : prevResults) {
                long long newAndResult = val & nums[i];
                if (newAndResult == k) {
                    count += freq;
                }
                currResults[newAndResult] += freq;
            }
            
            prevResults = currResults;
        }
        
        return count;
    }
};
"""


code3 = """
class Solution {
public:
    int numberOfAlternatingGroups(vector<int>& colors, int k) {
        vector<int> arr(colors.size()*2,0);
        int n=colors.size();
        for(int i=0;i<arr.size();i++){
            if(colors[i%n]!=colors[(i+1)%n]) arr[i]=1;
        }
        for(int i=1;i<arr.size();i++){
            arr[i]=arr[i]+arr[i-1];
        }
        int ans=0;
        for(int i=0;i<colors.size();i++){
            if(i==0){
            if(arr[i+(k-1)-1]==k-1) ans++;
            }
            else{
           if(arr[i+(k-1)-1]-arr[i-1]==k-1) ans++;
            }
        }
        return ans;
    }
};
"""


def checkPlagPercentage (code2, questionId) :
    if questionId == '4' : 
        final_output = Step2(code4, Step1(code2))
    elif questionId == '3' :
        final_output = Step2(code3, Step1(code2))

    return final_output
