#include <iostream>
#include <map>
#include <string>
#include <vector>

using i64 = long long;
using i128 = __int128_t;

static void print_i128(i128 x) {
  if (x == 0) {
    std::cout << "0\n";
    return;
  }
  bool neg = false;
  if (x < 0) {
    neg = true;
    x = -x;
  }
  char buf[64];
  int n = 0;
  while (x > 0) {
    buf[n++] = char('0' + int(x % 10));
    x /= 10;
  }
  if (neg) {
    std::cout << '-';
  }
  while (n--) {
    std::cout << buf[n];
  }
  std::cout << '\n';
}

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int T;
  std::cin >> T;
  while (T--) {
    int N;
    i64 K;
    std::cin >> N >> K;
    std::vector<i64> A(N), B(N), C(N), D(N);
    for (auto &x : A) {
      std::cin >> x;
    }
    for (auto &x : B) {
      std::cin >> x;
    }
    for (auto &x : C) {
      std::cin >> x;
    }
    for (auto &x : D) {
      std::cin >> x;
    }

    std::map<i64, i64> ms;
    i64 total = 0;
    i128 profit = 0;

    for (int i = 0; i < N; ++i) {
      i64 a = A[i], b = B[i], c = C[i], d = D[i];

      ms[-a] += b;
      total += b;

      i64 rem = d;
      while (rem > 0 && !ms.empty()) {
        auto it = std::prev(ms.end());
        i64 val = it->first;
        if (val + c <= 0) {
          break;
        }
        i64 cnt = it->second;
        i64 take = std::min(cnt, rem);
        profit += (i128)take * (i128)(val + c);
        if (cnt == take) {
          ms.erase(it);
        } else {
          it->second = cnt - take;
        }
        ms[-c] += take;
        rem -= take;
      }

      while (total > K && !ms.empty()) {
        auto it = ms.begin();
        i64 cnt = it->second;
        i64 drop = std::min(cnt, total - K);
        if (cnt == drop) {
          ms.erase(it);
        } else {
          it->second = cnt - drop;
        }
        total -= drop;
      }
    }

    print_i128(profit);
  }
  return 0;
}
