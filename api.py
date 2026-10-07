import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1"

def search_by_ingredients(ingredients):
    # TheMealDB only supports single-ingredient search
    # So we search each ingredient and merge results
    all_results = {}
    for ing in ingredients:
        url = f"{BASE_URL}/filter.php?i={ing}"
        r = requests.get(url).json()
        meals = r.get("meals")
        if meals:
            for m in meals:
                all_results[m["idMeal"]] = m
    return list(all_results.values())

def get_meal_details(meal_id):
    url = f"{BASE_URL}/lookup.php?i={meal_id}"
    r = requests.get(url).json()
    return r["meals"][0]

def list_categories():
    url = f"{BASE_URL}/list.php?c=list"
    return requests.get(url).json()["meals"]

def list_areas():
    url = f"{BASE_URL}/list.php?a=list"
    return requests.get(url).json()["meals"]

def list_tags(meal):
    tags = meal.get("strTags")
    if tags:
        return tags.split(",")
    return []
