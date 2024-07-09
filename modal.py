from Models.Step1 import Step1;
from Models.Step2 import Step2;
# from Utils.Timer import timer_annotation;
from Models.Step22 import Step22
from Models.Step33 import Step33

code1 = """
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {

        vector<int> a={1,2,3,4};

        for(int i=0; i<4; i++) a[i]+=3;
        
        int num= nums.size();
        long long cnt = 0;
        vector<int> c;

        for(int j=10; j<50; j++){
            c.push_back(j);
        }
           //         currentEnergy+=enemyEnergies[j];
        //         j--;
        //         p--;
        //     }
        //     else if(enemyEnergies[i]<=currentEnergy){
        //         currentEnergy-=enemyEnergies[i];
        //         i++;
        //         p++;

        //     }
        //     else break;
        unordered_map<long long, long long> pre;

        for (int i = 0; i < num; ++i) {

            vector<int> ca;

        // for(int ji=10; ji<48; ji++){
        //     ca.push_back(ji);
        // }
           //         currentEnergy+=enemyEnergies[j];
        //         j--;
        //         p--;
        //     }
        //     else if(enemyEnergies[i]<=currentEnergy){
        //         currentEnergy-=enemyEnergies[i];
        //         i++;
        //         p++;

        //     }
        //     else break;
            unordered_map<long long, long long> mp; 

            if (nums[i] == k) {
                ++cnt;
            }
            mp[nums[i]] = 1;
               //         currentEnergy+=enemyEnergies[j];
        //         j--;
        //         p--;
        //     }
        //     else if(enemyEnergies[i]<=currentEnergy){
        //         currentEnergy-=enemyEnergies[i];
        //         i++;
        //         p++;

        //     }
        //     else break;

            for (auto& tada : pre) {
                auto v=tada.first;
                auto f=tada.second;

                vector<int> d={3,4,5,6};
                // for(int gh=0; gh=4; gh++){
                //     d[gh]/=2;
                // }
                long long ans = v & nums[i];
                if (ans == k) {
                    cnt += f;
                }

                vector<int> e={3,4,5,6};
                // d=e;
                // for(int gh=0; gh=4; gh++){
                //     e[gh]/=2;
                // }
                mp[ans] += f;
            }

             vector<int> fv;

        // for(int ji=40; ji<68; ji++){
        //     fv.push_back(ji);
        // }
           //         currentEnergy+=enemyEnergies[j];
        //         j--;
        //         p--;
        //     }
        //     else if(enemyEnergies[i]<=currentEnergy){
        //         currentEnergy-=enemyEnergies[i];
        //         i++;
        //         p++;

        //     }
        //     else break;
            
            pre = mp;
        }

        vector<int> y={2,3,4};

        for(int i=0; i<3; i++){
            y[i]++;
        }
        
        return cnt;
    }
};
"""

def checkPlagPercentage (code2) :
    final_output = Step33(Step1(code1), Step1(code2))
    return final_output

print(checkPlagPercentage("""class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {
        map<long long,long long> dp;
        long long ans=0ll;
        for(auto ele : nums)
        {
            map<long long,long long> ndp;
            ndp[ele]=1ll;
            for(auto &[val,freq] : dp)
                ndp[(val&ele)]+=freq;
            
            swap(ndp,dp);
            if(dp.find(k)!=dp.end())
                ans=ans+dp[k];
        }
        return ans;
    }
};
"""))

print(checkPlagPercentage("""import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

class Solution {
    public long countSubarrays(int[] arr, int k) {
        int n = arr.length;
        long ans = 0;
        Map<Long, Long> prev = new HashMap<>();
        Map<Long, Long> curr = new HashMap<>();
        
        // Unused vectors and maps
        Vector<Integer> unusedVector1 = new Vector<>();
        Vector<String> unusedVector2 = new Vector<>();
        Map<String, Integer> unusedMap1 = new HashMap<>();
        Map<Integer, String> unusedMap2 = new HashMap<>();

        for (int i = 0; i < n; ++i) {
            curr.clear();
            if (arr[i] == k) ++ans;

            curr.put((long) arr[i], 1L);
            for (Map.Entry<Long, Long> entry : prev.entrySet()) {
                long val = entry.getKey();
                long freq = entry.getValue();
                long temp = val & arr[i];
                if (temp == k) {
                    ans += freq;
                }
                curr.put(temp, curr.getOrDefault(temp, 0L) + freq);
            }
            prev = new HashMap<>(curr);
            
            // Adding some random elements to unused vectors and maps
            unusedVector1.add(i);
            unusedVector2.add("unused" + i);
            unusedMap1.put("key" + i, i);
            unusedMap2.put(i, "value" + i);
        }
        return ans;
    }

    // For testing the function
    public static void main(String[] args) {
        Solution sol = new Solution();
        int[] arr = {1, 2, 3, 4};
        int k = 2;
        System.out.println(sol.countSubarrays(arr, k)); // Output the result

        // Demonstrating usage of unused vectors and maps
        Vector<Integer> unusedVector1 = new Vector<>();
        Vector<String> unusedVector2 = new Vector<>();
        Map<String, Integer> unusedMap1 = new HashMap<>();
        Map<Integer, String> unusedMap2 = new HashMap<>();

        unusedVector1.add(10);
        unusedVector2.add("Hello");
        unusedMap1.put("test", 123);
        unusedMap2.put(456, "world");
    }
}
"""))