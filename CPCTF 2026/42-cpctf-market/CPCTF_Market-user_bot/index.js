"use strict";

import { createServer } from "node:http";
import { chromium } from "playwright";

const PORT = 8081;
const ALLOW_ORIGINS = process.env.ALLOW_ORIGINS ? new RegExp(process.env.ALLOW_ORIGINS) : /^http:\/\/localhost(:\d+)?$/;
const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX_REQUESTS = 10;
const LOGIN_TIMEOUT_MS = 8_000;
const VIEW_DURATION_MS = 3_000;
const ACCOUNTS = JSON.parse(process.env.ACCOUNTS || "null") ?? [
  { accountId: "alice", password: "alice", pushKey: "alice-key" },
  { accountId: "bob", password: "bob", pushKey: "bob-key" },
];

let sharedBrowser = null;
let launchingBrowserPromise = null;

async function getSharedBrowser() {
  if (sharedBrowser?.isConnected()) return sharedBrowser;
  if (launchingBrowserPromise !== null) return launchingBrowserPromise;

  launchingBrowserPromise = chromium
    .launch({ headless: true })
    .then((browser) => {
      sharedBrowser = browser;
      browser.on("disconnected", () => {
        if (sharedBrowser === browser) sharedBrowser = null;
      });
      return browser;
    })
    .catch((error) => {
      sharedBrowser = null;
      throw error;
    })
    .finally(() => {
      launchingBrowserPromise = null;
    });

  return launchingBrowserPromise;
}

class User {
  constructor(accountId, password) {
    this.accountId = accountId;
    this.password = password;
    this.recentVisitTimesByUrl = new Map();
  }

  getRecentVisitTimes(url) {
    const now = Date.now();
    const recentVisitTimes = (this.recentVisitTimesByUrl.get(url) ?? []).filter(
      (visitedAt) => now - visitedAt < RATE_LIMIT_WINDOW_MS,
    );
    this.recentVisitTimesByUrl.set(url, recentVisitTimes);
    return recentVisitTimes;
  }

  canVisit(url) {
    return this.getRecentVisitTimes(url).length < RATE_LIMIT_MAX_REQUESTS;
  }

  async visit(url) {
    const recentVisitTimes = this.getRecentVisitTimes(url);
    recentVisitTimes.push(Date.now());
    this.recentVisitTimesByUrl.set(url, recentVisitTimes);

    console.log(`User ${this.accountId} is visiting ${url}`);

    const targetUrl = new URL(url);
    targetUrl.hash = "";
    const topPageUrl = new URL("/", targetUrl);

    const browser = await getSharedBrowser();
    const context = await browser.newContext();
    const page = await context.newPage();
    page.setDefaultTimeout(LOGIN_TIMEOUT_MS);
    page.setDefaultNavigationTimeout(LOGIN_TIMEOUT_MS);

    try {
      await page.goto(topPageUrl.href, { waitUntil: "domcontentloaded" });
      await page.fill('.login-form input[name="accountId"]', this.accountId);
      await page.fill('.login-form input[name="password"]', this.password);
      await page.click('.login-form button[type="submit"]');

      const loggedIn = await page
        .waitForSelector("body.authenticated", { timeout: LOGIN_TIMEOUT_MS })
        .then(() => true)
        .catch(() => false);

      if (!loggedIn) {
        const loginError = ((await page.textContent(".login-error")) || "").trim();
        throw new Error(loginError || "login failed");
      }

      if (this.accountId === "alice") {
        page.on("response", async (res) => {
          if (res.request().method() !== "GET") return;
          const url = new URL(res.url());
          if (!url.pathname.startsWith("/api/shops/")) return;
          const data = await res.json().catch(() => null);
          console.log(`[${url}]: ${JSON.stringify(data)}`);
        });
      }

      await page.goto(targetUrl.href, { waitUntil: "domcontentloaded" });
      await page.waitForTimeout(VIEW_DURATION_MS);
    } finally {
      await context.close();
    }
  }
}

// Comment for CTF contestants: Everything below this is non-essential and you do not really need to read it.

const users = new Map(ACCOUNTS.map(({ accountId, password, pushKey }) => [pushKey, new User(accountId, password)]));

const server = createServer((req, res) => {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }
  const key = req.headers["x-push-key"];
  if (typeof key !== "string" || !users.has(key)) {
    res.statusCode = 401;
    res.end("Unauthorized");
    return;
  }
  const user = users.get(key);

  let body = "";
  req.on("data", (chunk) => {
    body += chunk.toString();
    if (body.length > 2048) {
      res.statusCode = 413;
      res.end("Payload Too Large");
      req.destroy();
    }
  });
  req.on("end", () => {
    try {
      new URL(body);
    } catch {
      res.statusCode = 400;
      res.end("Bad Request");
      return;
    }
    const url = new URL(body);
    if (!ALLOW_ORIGINS.test(url.origin)) {
      res.statusCode = 403;
      res.end("Forbidden");
      return;
    }
    const href = url.href;

    if (!user.canVisit(href)) {
      res.statusCode = 429;
      res.end("Too Many Requests");
      return;
    }

    user.visit(href).catch((error) => {
      console.error(`Visit failed for user ${user.accountId}:`, error);
    });
    res.statusCode = 200;
    res.end("OK");
  });
});

server.listen(PORT, () => {
  console.log(`User BOT is listening on http://localhost:${PORT}`);
});
