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

procesed1 = Step1(code1)

def checkPlagPercentage (code2) :
    final_output = Step2(procesed1, Step1(code2))
    return final_output
