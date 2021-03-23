#include <bits/stdc++.h>
using namespace std;
#define FOR(i,a,b)  for(int i=(a);i<=(b);++i)
#define FORS(i,a,b) for(int i=(a);i<(b);++i)

int n, K;

int main()
{
    cin.tie(0);
    ios_base::sync_with_stdio(0);
    cin >> n >> K;
    vector<int> S(n);
    vector<int> dp(K + 1, 0);
    FORS (i, 0, n) {
        cin >> S[i];
    }
    FORS (i, 0, n) {
        for (int j = K; j >= S[i]; j--) {
            dp[j] = max(dp[j], S[i] + dp[j - S[i]]);
        }
    }
    cout << dp[K] << '\n';
}
