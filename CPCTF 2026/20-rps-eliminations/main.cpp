#include <array>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using u64 = unsigned long long;

namespace {

constexpr std::array<char, 3> CH = {'P', 'R', 'S'};
constexpr std::array<int, 3> LOSER = {1, 2, 0};
constexpr std::array<int, 3> BEAT = {2, 0, 1};

u64 add_cap(u64 a, u64 b, u64 cap) {
  if (a >= cap || b >= cap)
    return cap;
  u64 need = cap - a;
  return b >= need ? cap : a + b;
}

u64 mul_cap(u64 a, u64 b, u64 cap) {
  if (a == 0 || b == 0)
    return 0;
  __uint128_t prod = static_cast<__uint128_t>(a) * b;
  return prod >= cap ? cap : static_cast<u64>(prod);
}

u64 count_one_label(int leaves, u64 cap) {
  if (leaves <= 1)
    return 1;
  if (leaves - 1 >= 60)
    return cap;
  u64 v = 1ULL << (leaves - 1);
  return v >= cap ? cap : v;
}

bool enough_strings(int n, u64 k) {
  if (n - 1 >= 60)
    return true;
  return (1ULL << (n - 1)) >= k;
}

struct Fenwick {
  int n;
  std::vector<int> bit;

  explicit Fenwick(int n_) : n(n_), bit(n_ + 1, 0) {}

  void add(int idx, int delta) {
    for (; idx <= n; idx += idx & -idx)
      bit[idx] += delta;
  }

  int kth(int k) const {
    int idx = 0;
    int step = 1;
    while ((step << 1) <= n)
      step <<= 1;
    for (int jump = step; jump > 0; jump >>= 1) {
      int next = idx + jump;
      if (next <= n && bit[next] < k) {
        idx = next;
        k -= bit[next];
      }
    }
    return idx + 1;
  }
};

struct Ret {
  int label;
  u64 offset;
};

struct Frame {
  int node;
  u64 k;
  int phase;
  int left_label;
  std::array<u64, 3> w;
  std::array<u64, 3> bw;
  std::array<std::array<u64, 3>, 3> rw;
};

std::string solve_target(int root, int target, int n,
                         const std::vector<int> &lc, const std::vector<int> &rc,
                         const std::vector<int> &subtree_size, u64 k) {
  std::string answer;
  answer.reserve(n);

  std::vector<Frame> st;
  st.reserve(2 * n);
  Frame root_frame{};
  root_frame.node = root;
  root_frame.k = k;
  root_frame.phase = 0;
  root_frame.left_label = -1;
  root_frame.w = {0, 0, 0};
  root_frame.w[target] = 1;
  st.push_back(root_frame);

  Ret last{-1, 0};
  const u64 cap = k;

  while (!st.empty()) {
    Frame &f = st.back();
    if (f.phase == 0) {
      if (lc[f.node] == 0) {
        u64 used = 0;
        for (int label = 0; label < 3; ++label) {
          u64 cnt = f.w[label];
          if (f.k <= used + cnt) {
            answer.push_back(CH[label]);
            last = {label, f.k - used};
            break;
          }
          used += cnt;
        }
        st.pop_back();
        continue;
      }

      const int left = lc[f.node];
      const int right = rc[f.node];
      const u64 right_cnt = count_one_label(subtree_size[right], cap);
      for (int label = 0; label < 3; ++label) {
        auto &rw = f.rw[label];
        rw = {0, 0, 0};
        rw[LOSER[label]] = add_cap(rw[LOSER[label]], f.w[label], cap);
        rw[BEAT[label]] = add_cap(rw[BEAT[label]], f.w[BEAT[label]], cap);
        u64 sum = 0;
        for (int x = 0; x < 3; ++x)
          sum = add_cap(sum, rw[x], cap);
        f.bw[label] = mul_cap(sum, right_cnt, cap);
      }

      f.phase = 1;
      Frame next{};
      next.node = left;
      next.k = f.k;
      next.phase = 0;
      next.left_label = -1;
      next.w = f.bw;
      st.push_back(next);
      continue;
    }

    if (f.phase == 1) {
      f.left_label = last.label;
      f.phase = 2;
      Frame next{};
      next.node = rc[f.node];
      next.k = last.offset;
      next.phase = 0;
      next.left_label = -1;
      next.w = f.rw[f.left_label];
      st.push_back(next);
      continue;
    }

    int parent = -1;
    if (last.label == LOSER[f.left_label]) {
      parent = f.left_label;
    } else {
      parent = BEAT[f.left_label];
    }
    last = {parent, last.offset};
    st.pop_back();
  }

  return answer;
}

} // namespace

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int T;
  std::cin >> T;
  while (T--) {
    int N;
    u64 K;
    std::cin >> N >> K;

    std::vector<int> A(N);
    for (int i = 1; i <= N - 1; ++i)
      std::cin >> A[i];

    std::vector<int> lc(2 * N + 1, 0), rc(2 * N + 1, 0),
        subtree_size(2 * N + 1, 1);
    std::vector<int> slot(N + 1);
    Fenwick fw(N);
    for (int i = 1; i <= N; ++i) {
      slot[i] = i;
      fw.add(i, 1);
    }

    int nodes = N;
    for (int step = 1; step <= N - 1; ++step) {
      int p = fw.kth(A[step]);
      int q = fw.kth(A[step] + 1);
      ++nodes;
      lc[nodes] = slot[p];
      rc[nodes] = slot[q];
      subtree_size[nodes] = subtree_size[lc[nodes]] + subtree_size[rc[nodes]];
      slot[p] = nodes;
      fw.add(q, -1);
    }

    const int root = slot[fw.kth(1)];
    if (!enough_strings(N, K)) {
      std::cout << -1 << '\n' << -1 << '\n' << -1 << '\n';
      continue;
    }

    for (int target : {1, 0, 2})
      std::cout << solve_target(root, target, N, lc, rc, subtree_size, K)
                << '\n';
  }
  return 0;
}
