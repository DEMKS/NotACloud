#include <iostream>
#include <vector>
#include <cmath>
using namespace std;
int main()
{
    int n, d;
    vector <pair <int, bool> > v;
    cin >> n;
    for (int i = 0; i < n; i++){
        cin >> d;
        v.push_back({d, 0});
    }
    d = 0;
    d += v[1].first - v[0].first;
    v[0].second = 1;
    v[1].second = 1;
    for (int i = 1; i < n; i++){
        if (i + 2 < n){
            if (v[i + 2].first - v[i + 1].first < v[i + 1].first - v[i].first){
                d += v[i + 2].first - v[i + 1].first;
                v[i + 2].second = 1;
                v[i + 1].second = 1;
                i++;
            }else{
                d += v[i + 1].first - v[i].first;
            }
        }else{
            if (i + 1 < n){
                d += v[i + 1].first - v[i].first;
            }
        }
    }
    cout << d;
    return 0;
}
