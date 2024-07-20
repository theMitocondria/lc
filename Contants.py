BASE_URL = 'https://leetcode.com/contest/biweekly-contest-134/ranking/'
NUM_THREADS = 3  
STARTING_PAGE = 40
ENDING_PAGE = 60

STARTQUESTION = 6  # give 6 to sracp 3 and 4 give 7 to scrap only 4
ENDQUESTION = 8    # always remaing 8

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
        for (auto& [val, freq]: prevResults) {
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
    int numberOfAlternatingGroups(vector<int>& arr, int k) {
        int n=arr.size();
        vector<int> a(n+k-1);
        for(int i=0;i<n;i++)
        {
            a[i]=arr[i];
        }
        for(int i=n;i<n+k-1;i++)
        {
            a[i]=arr[i%n];
        }
        int i=0;int j=0;
        int expected;
        int len=0;
        int ans=0;
        while(j<a.size())
        {
            if(j==0)
            {
                expected=1-a[j];
                j++;
                len++;
                continue;
            }
            if(a[j]==expected)
            {
                len++;
                expected=1-expected;
            }
            else
            {
                len=1;
                expected=1-a[j];
            }
            if(j-i+1<k)
            {
                j++;
            }
            else if(j-i+1==k)
            {
                if(len>=k)
                {
                    ans++;
                }
                j++;
                i++;
            }
        }
        return ans;
    }
};
"""
