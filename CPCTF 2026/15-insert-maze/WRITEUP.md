# Insert Maze (Yukicoder No. 3504)

**Key reduction:** An optimal path can be taken as monotone, using only `right` and `down`. A left/up detour must later be canceled by a matching right/down detour, and here the only blocked cells are isolated original `#` cells, while every inserted-row / inserted-column cell is passable. So an optimal route never needs to decrease a coordinate.

**Doubled grid:** Between every adjacent original row/column, add a **potential** gap row/column. So we work on a `(2H-1) x (2W-1)` state grid.

- `(even, even)` = an original cell, blocked iff the original cell is `#`
- any state with an odd coordinate = a cell on an inserted row/column, always passable

From a state, there are only four useful monotone transitions:

- move right to the next original column directly: cost `1`
- move right into a gap column: cost `1`
- move down to the next original row directly: cost `1`
- move down into a gap row: cost `1`

In the doubled indexing this becomes:

- `(r, c) -> (r, c+1)` if `c+1` exists
- `(r, c) -> (r, c+2)` if `c` is even and `c+2` exists
- `(r, c) -> (r+1, c)` if `r+1` exists
- `(r, c) -> (r+2, c)` if `r` is even and `r+2` exists

provided the destination state is passable. The graph is a DAG because every edge goes right or down, so a simple DP in row-major order gives the shortest distance in `O(HW)`.

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int H, W;
    cin >> H >> W;
    vector<string> C(H);
    for (int i = 0; i < H; ++i) cin >> C[i];

    int RH = 2 * H - 1;
    int CW = 2 * W - 1;
    const int INF = 1e9;

    auto passable = [&](int r, int c) {
        if ((r & 1) == 0 && (c & 1) == 0) {
            return C[r / 2][c / 2] != '#';
        }
        return true;
    };

    vector<vector<int>> dp(RH, vector<int>(CW, INF));
    dp[0][0] = 0;

    for (int r = 0; r < RH; ++r) {
        for (int c = 0; c < CW; ++c) {
            if (dp[r][c] == INF || !passable(r, c)) continue;

            if (c + 1 < CW && passable(r, c + 1)) {
                dp[r][c + 1] = min(dp[r][c + 1], dp[r][c] + 1);
            }
            if ((c & 1) == 0 && c + 2 < CW && passable(r, c + 2)) {
                dp[r][c + 2] = min(dp[r][c + 2], dp[r][c] + 1);
            }
            if (r + 1 < RH && passable(r + 1, c)) {
                dp[r + 1][c] = min(dp[r + 1][c], dp[r][c] + 1);
            }
            if ((r & 1) == 0 && r + 2 < RH && passable(r + 2, c)) {
                dp[r + 2][c] = min(dp[r + 2][c], dp[r][c] + 1);
            }
        }
    }

    int ans = dp[RH - 1][CW - 1];
    cout << (ans == INF ? -1 : ans) << '\n';
    return 0;
}
```

**Why the direct `+2` edges are needed:** If you do **not** insert between two adjacent original rows/columns, moving to the next original row/column still costs exactly `1`. A plain BFS on the full doubled grid would incorrectly force you to pay `2` there.

**Samples:** Sample 1 becomes `5` by using one gap column. Sample 2 stays `2` with no insertions. Sample 3 gives `8`.

**Contest note:** This is the ACM-style task, so there is no separate jeopardy flag here; the goal is just to get AC.
