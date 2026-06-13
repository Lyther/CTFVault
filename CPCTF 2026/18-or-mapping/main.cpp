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
    if (vis[s])
      continue;
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
  comps.reserve(N);
  for (int it = N - 1; it >= 0; --it) {
    int s = order[it];
    if (comp[s] != -1)
      continue;
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
      if (cu != cv)
        dag_edges.push_back({cu, cv});
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

  // type: 0 = singleton SCC, 1 = odd-cycle SCC, -1 = bad even-period SCC
  vector<int> type(C, 0);
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
        if (comp[v] != cid)
          continue;
        int want = color[u] ^ 1;
        if (color[v] == -1) {
          color[v] = want;
          dq.push_back(v);
        } else if (color[v] != want) {
          odd_cycle = true;
        }
      }
    }

    for (int u : comps[cid])
      color[u] = -1;
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
    if (indeg2[cid] == 0)
      tq.push(cid);
  }

  vector<int> topo;
  topo.reserve(C);
  while (!tq.empty()) {
    int u = tq.front();
    tq.pop();
    topo.push_back(u);
    for (int v : dag[u]) {
      if (--indeg2[v] == 0)
        tq.push(v);
    }
  }

  const int NEG = -1000000000;
  vector<int> dp(C, NEG);
  dp[start] = 1;
  for (int u : topo) {
    if (dp[u] < 0)
      continue;
    for (int v : dag[u]) {
      if (type[u] == 0 && type[v] == 0)
        continue;
      dp[v] = max(dp[v], dp[u] + 1);
    }
  }

  int best = 0;
  for (int x : dp)
    best = max(best, x);
  cout << (best == C ? "Yes\n" : "No\n");
  return 0;
}
