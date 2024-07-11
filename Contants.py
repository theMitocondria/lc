BASE_URL = 'https://leetcode.com/contest/biweekly-contest-134/ranking/'
NUM_THREADS = 3  
STARTING_PAGE = 52
ENDING_PAGE = 100

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
"""
