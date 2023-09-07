# Get a list of recipe names
def get_recipe_names(soup):
    recipe_names_list = []
    recipe_names = soup.find_all('h2', attrs={'class':'heading-4'})
    for name in recipe_names:
        recipe_names_list.append(name.text)
    recipe_names_list.pop()
    return recipe_names_list