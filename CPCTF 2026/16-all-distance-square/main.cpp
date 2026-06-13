#include <algorithm>
#include <bitset>
#include <cassert>
#include <iostream>
#include <vector>

using namespace std;

static constexpr int MAX_N = 100;
static constexpr int MAX_SUM = 50000;

using BS = bitset<MAX_SUM + 1>;

struct Edge {
  int u;
  int v;
  int w;
};

static BS sq_bits;
static BS dp[MAX_N + 1][MAX_N + 1];
static int xw[MAX_N + 1];
static int yw[MAX_N + 1];
static int eid_x[MAX_N + 1];
static int eid_y[MAX_N + 1];
static vector<Edge> edges;

static void init_squares() {
  for (int i = 1; i * i <= MAX_SUM; ++i) {
    sq_bits.set(i * i);
  }
}

static bool has_square(const BS &bits) { return (bits & sq_bits).any(); }

static void build_graph() {
  init_squares();

  edges = {
      {1, 2, 16},
      {2, 3, 9},
      {1, 3, 25},
  };

  xw[1] = 16;
  xw[2] = 9;
  yw[1] = 25;
  eid_x[1] = 1;
  eid_x[2] = 2;
  eid_y[1] = 3;

  vector<int> used(201, 0);
  used[16] = used[9] = used[25] = 1;

  dp[2][1].set(16);
  dp[3][1].set(25);
  dp[3][1].set(16 + 9);
  dp[3][2].set(9);
  dp[3][2].set(16 + 25);

  int n = 3;
  int next_id = 4;
  while (n < MAX_N) {
    int a = -1;
    int b = -1;
    for (int ca = 1; ca <= 200 && a == -1; ++ca) {
      if (used[ca]) {
        continue;
      }
      for (int cb = 1; cb <= 200; ++cb) {
        if (used[cb] || cb == ca) {
          continue;
        }

        bool ok = true;
        for (int s = 1; s <= n - 2; ++s) {
          BS bits = (dp[n][s] << ca) | (dp[n - 1][s] << cb);
          if (!has_square(bits)) {
            ok = false;
            break;
          }
        }
        if (!ok) {
          continue;
        }

        {
          BS bits = (dp[n][n - 1] << ca);
          bits.set(cb);
          if (!has_square(bits)) {
            continue;
          }
        }
        {
          BS bits = (dp[n][n - 1] << cb);
          bits.set(ca);
          if (!has_square(bits)) {
            continue;
          }
        }

        a = ca;
        b = cb;
        break;
      }
    }

    assert(a != -1 && b != -1);

    xw[n] = a;
    yw[n - 1] = b;
    eid_x[n] = next_id++;
    eid_y[n - 1] = next_id++;
    edges.push_back({n, n + 1, a});
    edges.push_back({n - 1, n + 1, b});
    used[a] = used[b] = 1;

    ++n;
    for (int s = 1; s <= n - 3; ++s) {
      dp[n][s] = (dp[n - 1][s] << a) | (dp[n - 2][s] << b);
    }
    dp[n][n - 2] = (dp[n - 1][n - 2] << a);
    dp[n][n - 2].set(b);
    dp[n][n - 1] = (dp[n - 1][n - 2] << b);
    dp[n][n - 1].set(a);
  }
}

static int pick_square_sum(int i, int j) {
  for (int s = 1; s * s <= MAX_SUM; ++s) {
    int sq = s * s;
    if (dp[j][i].test(sq)) {
      return sq;
    }
  }
  return -1;
}

static vector<int> build_path(int i, int j, int target) {
  if (j == 2 && i == 1) {
    return {eid_x[1]};
  }

  if (i <= j - 3) {
    if (target >= xw[j - 1] && dp[j - 1][i].test(target - xw[j - 1])) {
      auto res = build_path(i, j - 1, target - xw[j - 1]);
      res.push_back(eid_x[j - 1]);
      return res;
    }
    auto res = build_path(i, j - 2, target - yw[j - 2]);
    res.push_back(eid_y[j - 2]);
    return res;
  }

  if (i == j - 2) {
    if (target == yw[j - 2]) {
      return {eid_y[j - 2]};
    }
    auto res = build_path(i, j - 1, target - xw[j - 1]);
    res.push_back(eid_x[j - 1]);
    return res;
  }

  assert(i == j - 1);
  if (target == xw[j - 1]) {
    return {eid_x[j - 1]};
  }
  auto res = build_path(j - 2, j - 1, target - yw[j - 2]);
  reverse(res.begin(), res.end());
  res.push_back(eid_y[j - 2]);
  return res;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  build_graph();

  int N;
  cin >> N;

  cout << 2 * N - 3 << '\n';
  for (int i = 0; i < 2 * N - 3; ++i) {
    cout << edges[i].u << ' ' << edges[i].v << ' ' << edges[i].w << '\n';
  }

  for (int i = 1; i <= N; ++i) {
    for (int j = i + 1; j <= N; ++j) {
      int sq = pick_square_sum(i, j);
      assert(sq != -1);
      auto path = build_path(i, j, sq);
      cout << path.size();
      for (int id : path) {
        cout << ' ' << id;
      }
      cout << '\n';
    }
  }

  return 0;
}
