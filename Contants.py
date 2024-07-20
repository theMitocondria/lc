BASE_URL = 'https://leetcode.com/contest/biweekly-contest-135/ranking/'
NUM_THREADS = 3  
STARTING_PAGE = 25  #95
ENDING_PAGE = 95    #163

STARTQUESTION = 6  # give 6 to sracp 3 and 4 give 7 to scrap only 4
ENDQUESTION = 7   # always remaing 8

code4 = """ 
"""

code3 = """
class Solution {
public:
    int minChanges(std::vector<int>& nums, int k) {
        std::map<int, std::vector<int>> m;
        std::vector<int> v;

        for (int i = 0; i < nums.size() / 2; ++i) {
            int a = nums[i];
            int b = nums[nums.size() - i - 1];
            int diff = std::abs(a - b);
             int X = std::max({a, b, k - a, k - b});
             m[diff].push_back(X);
            v.push_back(X);
        }

        int ans = nums.size();  
        std::sort(v.begin(), v.end());

        for (const auto& [diff, values] : m) {
            int T = std::lower_bound(v.begin(), v.end(), diff) - v.begin();
            T = T * 2 + (nums.size() / 2 - T);
            for (const auto& X : values) {
                if (X < diff) {
                    T -= 2;
                } else {
                    T -= 1;
                }
            }
            ans = std::min(ans, T);
        }

        return ans;
}
};
"""
