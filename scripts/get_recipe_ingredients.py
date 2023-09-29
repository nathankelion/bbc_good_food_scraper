# Get the ingredients
def get_recipe_ingredients(soup):
    recipe_ingredients = []
    ingredients = soup.find_all('li', attrs={'class': 'pb-xxs pt-xxs list-item list-item--separator'})
    for ingredient in ingredients:
        recipe_ingredients.append(ingredient.text)
    return recipe_ingredients