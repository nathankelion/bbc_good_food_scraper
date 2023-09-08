# Get recipe name
def get_recipe_name(soup):
    recipe_name = soup.find('h1', attrs={'class':'heading-1'})
    return recipe_name.text