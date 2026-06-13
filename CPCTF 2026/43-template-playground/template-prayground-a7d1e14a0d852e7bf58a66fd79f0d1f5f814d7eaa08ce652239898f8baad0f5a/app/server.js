const express = require("express");
const _ = require("lodash");
const path = require("path");
const acorn = require("acorn");

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const helpers = {
  upper: (s) => String(s).toUpperCase(),
  lower: (s) => String(s).toLowerCase(),
  reverse: (s) => String(s).split("").reverse().join(""),
  repeat: (s, n) => String(s).repeat(Number(n) || 2),
};

app.get("/api/helpers", (req, res) => {
  res.json({ available: Object.keys(helpers) });
});

const FORBIDDEN_IDS = new Set([
  "eval",
  "Function",
  "AsyncFunction",
  "GeneratorFunction",
]);

function isAllowedIdent(node) {
  return node.type === "Identifier" && !FORBIDDEN_IDS.has(node.name);
}

function isAllowedExpr(node) {
  if (!node) return false;
  if (node.type === "Identifier") return isAllowedIdent(node);
  if (node.type === "CallExpression") {
    if (!isAllowedIdent(node.callee)) return false;
    return node.arguments.every(isAllowedIdent);
  }
  return false;
}

function validateInterpolation(src) {
  let ast;
  try {
    ast = acorn.parse(src, { ecmaVersion: 2022 });
  } catch {
    return false;
  }
  if (ast.body.length !== 1) return false;
  if (ast.body[0].type !== "ExpressionStatement") return false;
  return isAllowedExpr(ast.body[0].expression);
}

function validateTemplate(tmpl) {
  const re = /<%(=|-)?([\s\S]*?)%>|\$\{([^\\}]*(?:\\.[^\\}]*)*)\}/g;
  let m;
  while ((m = re.exec(tmpl)) !== null) {
    if (m[0].startsWith("<%")) {
      const kind = m[1];
      const body = m[2];
      if (!kind) return "evaluate blocks (<% %>) are not allowed";
      if (!validateInterpolation(body)) {
        return "interpolation must be a bare identifier or a simple function call";
      }
    } else {
      // ${} — also validated the same way
      if (!validateInterpolation(m[3])) {
        return "interpolation must be a bare identifier or a simple function call";
      }
    }
  }
  return null;
}

app.post("/api/render", (req, res) => {
  const { template: tmpl, data, use } = req.body;

  if (!tmpl || typeof tmpl !== "string") {
    return res.status(400).json({ error: "template is required" });
  }
  if (tmpl.length > 500) {
    return res.status(400).json({ error: "template too long" });
  }

  const syntaxError = validateTemplate(tmpl);
  if (syntaxError) {
    return res.status(400).json({ error: syntaxError });
  }

  const imports = {};
  if (Array.isArray(use)) {
    for (const name of use) {
      if (typeof name === "string" && name.length < 200) {
        imports[name] = helpers[name];
      }
    }
  }

  try {
    const compiled = _.template(tmpl, { imports, interpolate: /<%=([\s\S]+?)%>/g });
    const result = compiled(data || {});

    res.json({ html: result });
  } catch (err) {
    res.status(500).json({ error: "Failed to render template" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
