package main

import (
	"html/template"
	"log"
	"net/http"
	"os"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Recipe struct {
	gorm.Model
	Title       string
	Description string
}

var db *gorm.DB

var indexTmpl = template.Must(template.New("index").Parse(`<!DOCTYPE html>
<html>
<head>
  <title>Hidden Recipe</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
</head>
<body>
<h1>Recipes</h1>
<form action="/search" method="get">
  <input type="text" name="q" placeholder="Search recipes...">
  <button type="submit">Search</button>
</form>
</body>
</html>`))

var searchTmpl = template.Must(template.New("search").Parse(`<!DOCTYPE html>
<html>
<head>
  <title>Hidden Recipe</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
</head>
<body>
<h1>Recipes</h1>
<form action="/search" method="get">
  <input type="text" name="q" placeholder="Search recipes...">
  <button type="submit">Search</button>
</form>
{{if .}}
<ul>
{{range .}}
  <li>
    <h2>{{.Title}}</h2>
    <p>{{.Description}}</p>
  </li>
{{end}}
</ul>
{{else}}
<p>No recipes found.</p>
{{end}}
</body>
</html>`))

func main() {
	var err error
	db, err = gorm.Open(sqlite.Open("recipes.db"), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	}

	db.AutoMigrate(&Recipe{})
	seed()

	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/search", searchHandler)
	log.Fatal(http.ListenAndServe(":80", nil))
}

func seed() {
	recipes := []Recipe{
		{Title: "Tomato Pasta", Description: "Boil pasta. Make sauce with tomatoes, garlic, and olive oil. Mix together."},
		{Title: "Chicken Curry", Description: "Cook chicken with curry powder, coconut milk, and vegetables. Serve with rice."},
		{Title: "Caesar Salad", Description: "Mix romaine lettuce with croutons, parmesan, and Caesar dressing."},
		{Title: "Grilled Salmon", Description: "Season salmon with salt and pepper. Grill for 4 minutes each side."},
		{Title: "Miso Soup", Description: "Dissolve miso paste in dashi broth. Add tofu and wakame seaweed."},
	}
	db.Create(&recipes)

	secret := Recipe{Title: "Secret Recipe", Description: os.Getenv("FLAG")}
	db.Create(&secret)
	db.Delete(&secret)
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	indexTmpl.Execute(w, nil)
}

func searchHandler(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("q")
	var recipes []Recipe
	db.Where("title LIKE '%" + q + "%'").Find(&recipes)
	searchTmpl.Execute(w, recipes)
}
