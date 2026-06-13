import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { desc, eq } from "drizzle-orm";
import { Hono } from "hono";
import { getCookie, setCookie } from "hono/cookie";
import { sign, verify } from "hono/jwt";
import { db } from "./db.js";
import { posts, users } from "./schema.js";

const JWT_SECRET = process.env.JWT_SECRET || "test-secret";

type ProfileUpdate = {
  displayName: string;
  bio: string;
};

function findUserById(id: number) {
  return db.select().from(users).where(eq(users.id, id)).get();
}

function findUserByUsername(username: string) {
  return db.select().from(users).where(eq(users.username, username)).get();
}

function createUser(username: string, password: string) {
  return db
    .insert(users)
    .values({ username, password, displayName: username })
    .returning()
    .get();
}

function updateProfile(id: number, data: ProfileUpdate) {
  db.update(users).set(data).where(eq(users.id, id)).run();
}

function createPost(userId: number, content: string) {
  return db
    .insert(posts)
    .values({ userId, content, createdAt: new Date().toISOString() })
    .returning()
    .get();
}

function getAllPosts() {
  return db
    .select({
      id: posts.id,
      content: posts.content,
      createdAt: posts.createdAt,
      userId: posts.userId,
      displayName: users.displayName,
      username: users.username,
      plan: users.plan,
    })
    .from(posts)
    .innerJoin(users, eq(posts.userId, users.id))
    .orderBy(desc(posts.createdAt))
    .all();
}

const app = new Hono();

const getUser = async (c: any) => {
  const token = getCookie(c, "token");
  if (!token) return null;
  try {
    const payload = await verify(token, JWT_SECRET, "HS256");
    return findUserById(payload.userId as number);
  } catch {
    return null;
  }
};

app.post("/api/register", async (c) => {
  const { username, password } = await c.req.json();
  if (!username || !password) return c.json({ error: "Missing fields" }, 400);

  try {
    const user = createUser(username, password);

    const token = await sign({ userId: user.id }, JWT_SECRET);
    setCookie(c, "token", token, { path: "/", httpOnly: true });
    return c.json({
      id: user.id,
      username: user.username,
      displayName: user.displayName,
      bio: user.bio,
      plan: user.plan,
    });
  } catch {
    return c.json({ error: "Username already taken" }, 400);
  }
});

app.post("/api/login", async (c) => {
  const { username, password } = await c.req.json();
  const user = findUserByUsername(username);

  if (!user || user.password !== password) {
    return c.json({ error: "Invalid credentials" }, 401);
  }

  const token = await sign({ userId: user.id }, JWT_SECRET);
  setCookie(c, "token", token, { path: "/", httpOnly: true });
  return c.json({
    id: user.id,
    username: user.username,
    displayName: user.displayName,
    bio: user.bio,
    plan: user.plan,
  });
});

app.post("/api/logout", (c) => {
  setCookie(c, "token", "", { path: "/", maxAge: 0 });
  return c.json({ ok: true });
});

app.get("/api/me", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);

  return c.json({
    id: user.id,
    username: user.username,
    displayName: user.displayName,
    bio: user.bio,
    plan: user.plan,
  });
});

app.put("/api/me", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);

  const body: ProfileUpdate = await c.req.json();

  try {
    updateProfile(user.id, body);
  } catch {
    return c.json({ error: "Update failed" }, 400);
  }

  const updated = findUserById(user.id)!;

  return c.json({
    id: updated.id,
    username: updated.username,
    displayName: updated.displayName,
    bio: updated.bio,
    plan: updated.plan,
  });
});

app.get("/api/flag", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);
  if (user.plan !== "premium") {
    return c.json({ error: "Premium required" }, 403);
  }

  return c.json({ flag: process.env.FLAG || "CPCTF{dummy}" });
});

// Payment always fails because this is a CTF challenge.
app.post("/api/upgrade", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);

  return c.json(
    { error: "Payment failed. Please check your card details." },
    402,
  );
});

app.post("/api/posts", async (c) => {
  const user = await getUser(c);
  if (!user) return c.json({ error: "Unauthorized" }, 401);

  const { content } = await c.req.json();
  if (!content) return c.json({ error: "Content required" }, 400);

  return c.json(createPost(user.id, content));
});

app.get("/api/posts", (c) => {
  return c.json(getAllPosts());
});

app.use("/*", serveStatic({ root: "./public" }));
app.get("/*", serveStatic({ root: "./public", path: "/index.html" }));

const port = Number(process.env.PORT) || 3000;
serve({ fetch: app.fetch, port }, () => {
  console.log(`Server running on port ${port}`);
});
