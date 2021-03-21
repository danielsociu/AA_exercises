#include <bits/stdc++.h>
using namespace std;
#define FOR(i,a,b)  for(int i=(a);i<=(b);++i)
#define FORS(i,a,b) for(int i=(a);i<(b);++i)

int K, x, answer = 0;

int main()
{
    cin.tie(0);
    ios_base::sync_with_stdio(0);
    freopen("data.txt","r",stdin);
    cin >> K >> K;
    while(cin >> x) {
        answer = answer + x;
        if (answer > K) {
            answer = answer - x;
            if (x > answer) { // the secret behind 1/2 optimal 
                answer = x; // if the sum is > K then one 
            }               // value is >= than half
        }
    }
    cout << answer << '\n';
}
