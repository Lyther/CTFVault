# OR Mapping (Yukicoder No. 3508)

**Note:** The operation uses `T mod 2^K` and the target is `2^K - 1`. The pasted statement had some `2K` mojibake, but the official problem is the binary-power version.

**SCC viewpoint:** Compress the graph into its SCC DAG. During the walk, once you leave an SCC you can never come back, so the SCCs visited by the token must form a single directed path starting from `SCC(1)`. Therefore, to visit every vertex at all, the condensation DAG must have a Hamiltonian path starting from `SCC(1)`.

**Two SCC types:**

- **Point SCC:** a singleton SCC. It has no cycle, so its only vertex is visited at most once. Hence that vertex becomes full iff the arrival time is exactly `2^K-1 (mod 2^K)`.
- **Cycle SCC:** an SCC of size at least `2`. Let `g` be the gcd of lengths of directed cycles inside it.
  - If `g` is **odd**, then because `gcd(g, 2^K)=1`, standard periodicity says every residue modulo `2^K` can be realized on arrivals to any vertex, so we can make every vertex in that SCC full and also leave the SCC at any residue we want.
  - If `g` is **even**, then all walk lengths inside the SCC have fixed parity classes. Since the SCC has at least one edge, both parities appear among its vertices, so some vertex is only visited at even times and never gets bit `0`. Such an SCC is impossible.

So every non-singleton SCC must be an **odd-cycle SCC**.

**Path rule:** Along the SCC path,

- the first SCC must be an odd-cycle SCC, otherwise vertex `1` is never updated enough;
- two singleton SCCs cannot be consecutive:
  - entering a singleton must happen at time `2^K-1`,
  - the next move then has time `0`,
  - so the next singleton would fail immediately.

Conversely, if the SCC DAG has a Hamiltonian path from `SCC(1)` in which every non-singleton SCC is odd-cycle and no two singleton SCCs are consecutive, then it is feasible:

- inside each odd-cycle SCC, finish all its vertices and choose the exit residue freely;
- if the next SCC is a singleton, choose the exit so that the next arrival is `2^K-1`;
- after a singleton, the residue is forced to `0`, which is fine because the next SCC must be an odd-cycle SCC.

That makes the answer depend only on the SCC DAG and odd/even cycle parity. `K` itself does not affect the decision.

**Algorithm:**

1. Compute SCCs.
2. Build the condensation DAG.
3. Classify each SCC:
   - size `1` -> singleton type,
   - size `>=2` -> check whether it contains an odd directed cycle.
     This is just parity consistency on internal edges: assign `color[v] = distance mod 2`; if any edge violates `color[to] = color[from] ^ 1`, then an odd cycle exists.
4. From `SCC(1)`, all SCCs must be reachable.
5. Run longest-path DP on the condensation DAG from `SCC(1)`, forbidding transitions `singleton -> singleton` and forbidding bad even-cycle SCCs.
6. Answer `Yes` iff the longest valid path length equals the number of SCCs.

**Time / memory:** `O(N + M)`.

```cpp
#include <algorithm>
#include <deque>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int N, M, K;
  cin >> N >> M >> K;

  vector<vector<int>> adj(N + 1), radj(N + 1);
  for (int i = 0; i < M; ++i) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    radj[v].push_back(u);
  }

  vector<char> vis(N + 1, 0);
  vector<int> order;
  order.reserve(N);
  for (int s = 1; s <= N; ++s) {
    if (vis[s]) continue;
    vector<pair<int, int>> st;
    st.push_back({s, 0});
    vis[s] = 1;
    while (!st.empty()) {
      int u = st.back().first;
      int &idx = st.back().second;
      if (idx < (int)adj[u].size()) {
        int v = adj[u][idx++];
        if (!vis[v]) {
          vis[v] = 1;
          st.push_back({v, 0});
        }
      } else {
        order.push_back(u);
        st.pop_back();
      }
    }
  }

  vector<int> comp(N + 1, -1);
  vector<vector<int>> comps;
  for (int it = N - 1; it >= 0; --it) {
    int s = order[it];
    if (comp[s] != -1) continue;
    int cid = (int)comps.size();
    comps.push_back({});
    vector<int> st = {s};
    comp[s] = cid;
    while (!st.empty()) {
      int u = st.back();
      st.pop_back();
      comps[cid].push_back(u);
      for (int v : radj[u]) {
        if (comp[v] == -1) {
          comp[v] = cid;
          st.push_back(v);
        }
      }
    }
  }

  int C = (int)comps.size();
  vector<pair<int, int>> dag_edges;
  dag_edges.reserve(M);
  for (int u = 1; u <= N; ++u) {
    for (int v : adj[u]) {
      int cu = comp[u];
      int cv = comp[v];
      if (cu != cv) dag_edges.push_back({cu, cv});
    }
  }
  sort(dag_edges.begin(), dag_edges.end());
  dag_edges.erase(unique(dag_edges.begin(), dag_edges.end()), dag_edges.end());

  vector<vector<int>> dag(C);
  vector<int> indeg(C, 0);
  for (auto [u, v] : dag_edges) {
    dag[u].push_back(v);
    ++indeg[v];
  }

  vector<int> type(C, 0);
  // type: 0 = singleton, 1 = odd-cycle SCC, -1 = bad even-period SCC
  vector<int> color(N + 1, -1);
  for (int cid = 0; cid < C; ++cid) {
    if ((int)comps[cid].size() == 1) {
      type[cid] = 0;
      continue;
    }

    deque<int> dq;
    int root = comps[cid][0];
    dq.push_back(root);
    color[root] = 0;
    bool odd_cycle = false;

    while (!dq.empty()) {
      int u = dq.front();
      dq.pop_front();
      for (int v : adj[u]) {
        if (comp[v] != cid) continue;
        int want = color[u] ^ 1;
        if (color[v] == -1) {
          color[v] = want;
          dq.push_back(v);
        } else if (color[v] != want) {
          odd_cycle = true;
        }
      }
    }

    for (int u : comps[cid]) color[u] = -1;
    type[cid] = odd_cycle ? 1 : -1;
  }

  int start = comp[1];
  if (type[start] != 1) {
    cout << "No\n";
    return 0;
  }

  vector<char> reach(C, 0);
  queue<int> q;
  q.push(start);
  reach[start] = 1;
  int reach_cnt = 0;
  while (!q.empty()) {
    int u = q.front();
    q.pop();
    ++reach_cnt;
    for (int v : dag[u]) {
      if (!reach[v]) {
        reach[v] = 1;
        q.push(v);
      }
    }
  }

  if (reach_cnt != C) {
    cout << "No\n";
    return 0;
  }
  for (int cid = 0; cid < C; ++cid) {
    if (type[cid] == -1) {
      cout << "No\n";
      return 0;
    }
  }

  queue<int> tq;
  vector<int> indeg2 = indeg;
  for (int cid = 0; cid < C; ++cid) {
    if (indeg2[cid] == 0) tq.push(cid);
  }
  vector<int> topo;
  topo.reserve(C);
  while (!tq.empty()) {
    int u = tq.front();
    tq.pop();
    topo.push_back(u);
    for (int v : dag[u]) {
      if (--indeg2[v] == 0) tq.push(v);
    }
  }

  const int NEG = -1e9;
  vector<int> dp(C, NEG);
  dp[start] = 1;
  for (int u : topo) {
    if (dp[u] < 0) continue;
    for (int v : dag[u]) {
      if (type[u] == 0 && type[v] == 0) continue;
      dp[v] = max(dp[v], dp[u] + 1);
    }
  }

  int best = 0;
  for (int x : dp) best = max(best, x);
  cout << (best == C ? "Yes\n" : "No\n");
  return 0;
}
```

**Samples:** The 3-cycle in sample 1 is one odd-cycle SCC, so `Yes`. Sample 2 has only singleton SCCs in a DAG, so the start SCC is already invalid and the answer is `No`.

**Contest note:** This is the ACM-style task, so there is no separate jeopardy flag here; the goal is just to get AC.
