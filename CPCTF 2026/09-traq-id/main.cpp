#include <bits/stdc++.h>
using namespace std;

static bool allowed(unsigned char c) {
  if (isalnum(c))
    return true;
  return c == '_' || c == '-';
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  if (!(cin >> s))
    return 0;

  if (s.size() < 1 || s.size() > 32) {
    cout << "400\n";
    return 0;
  }
  for (unsigned char c : s) {
    if (!allowed(c)) {
      cout << "400\n";
      return 0;
    }
  }
  if (s.front() == '_' || s.front() == '-' || s.back() == '_' ||
      s.back() == '-') {
    cout << "400\n";
    return 0;
  }
  cout << "200\n";
  return 0;
}
